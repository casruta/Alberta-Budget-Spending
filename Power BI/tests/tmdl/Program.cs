using Microsoft.AnalysisServices.Tabular;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

if (args.Length != 2) throw new ArgumentException("Usage: TmdlCheck <definition folder> <receipt.json>");
var folder=Path.GetFullPath(args[0]);
var database=TmdlSerializer.DeserializeDatabaseFromFolder(folder);
var model=database.Model;
if(database.CompatibilityLevel != 1601 || model.Tables.Count != 68 || model.Relationships.Count != 0 || model.DataSources.Count != 0)
    throw new Exception("Unexpected model topology");
if(model.Tables.Count(t => t.IsHidden) != 66) throw new Exception("Expected 66 hidden original evidence tables");
foreach(var table in model.Tables)
{
    foreach(var column in table.Columns.OfType<DataColumn>())
        if(column.SourceColumn != column.Name) throw new Exception($"SourceColumn mismatch: {table.Name}.{column.Name} -> {column.SourceColumn}");
    if(table.Partitions.Count != 1 || table.Partitions[0].Source is not MPartitionSource || table.Partitions[0].Mode != ModeType.Import)
        throw new Exception("Expected embedded M import partition: "+table.Name);
}
var facts=model.Tables["ChartData"];
if(facts.Columns["Value"].DataType != DataType.Double) throw new Exception("Plotted values must be numeric");
if(facts.Measures["Chart value"].Expression != "IF(COUNTROWS(ChartData) = 1, MAX(ChartData[Value]), BLANK())")
    throw new Exception("Unexpected aggregation semantics");
if(facts.Measures["Chart value"].FormatStringDefinition is null) throw new Exception("Expected unit-aware display formatting");
var fingerprint=new StringBuilder();
foreach(var file in Directory.GetFiles(folder,"*.tmdl",SearchOption.AllDirectories).OrderBy(f => Path.GetRelativePath(folder,f),StringComparer.Ordinal))
    fingerprint.Append(Path.GetRelativePath(folder,file).Replace(Path.DirectorySeparatorChar,'/')).Append('\n').Append(Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(file))).ToLowerInvariant()).Append('\n');
var receipt=new {
    tool="Microsoft.AnalysisServices.Tabular.TmdlSerializer.DeserializeDatabaseFromFolder",
    nuget_package="Microsoft.AnalysisServices 19.113.2",
    compatibility_level=database.CompatibilityLevel,
    model_tables=model.Tables.Count,
    hidden_evidence_tables=model.Tables.Count(t => t.IsHidden),
    relationships=model.Relationships.Count,
    external_data_sources=model.DataSources.Count,
    source_column_bindings_verified=true,
    native_tmdl_parse_passed=true,
    definition_sha256=Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(fingerprint.ToString()))).ToLowerInvariant(),
    limits="Parses native TMDL and checks model metadata; does not evaluate M/DAX or render Power BI Desktop visuals."
};
File.WriteAllText(args[1],System.Text.Json.JsonSerializer.Serialize(receipt,new JsonSerializerOptions {WriteIndented=true})+"\n");
Console.WriteLine($"Native TMDL parser passed: {model.Tables.Count} tables, embedded import partitions, source-column bindings and numeric chart values verified.");
