# Source receipt and retrieval diagnosis

All current PDFs below were retrieved from links on the official Alberta annual-report index. The current poverty extract was downloaded directly from Statistics Canada. Existing repository PDFs are archived official publications, not newly downloaded in this loop.

## Retrieval results

The official annual-report and budget-document indexes returned HTTP200. Python urllib requests for several PDF resources returned403; a diagnosis-driven comparison with curl -L --fail on the same official URL succeeded200 using the normal proxy and TLS verification. Earlier failures are retained in manifests but superseded for successfully downloaded resources. No authentication, TLS, proxy or access-control bypass was used. A Statistics Canada topic hub still returned a proxy denial, and one survey metadata endpoint returned403; neither prevents using the successfully retrieved table/metadata. No unavailable content is cited as reviewed.

|Source identity|Local PDF|Pages|Official download|
|---|---|---:|---|
|Education Annual Report Update 2024-2025|[ecc-annual-report-update-2024-2025.pdf](../education_safety/ecc-annual-report-update-2024-2025.pdf)|20|[Government source](https://open.alberta.ca/dataset/8d78df56-9979-457c-9ec2-26e87bd922ed/resource/8130ef49-31fd-473b-affa-9b5fb81f1726/download/ecc-annual-report-update-2024-2025.pdf)|
|Education Annual Report 2024-2025|[educ-annual-report-2024-2025.pdf](../education_safety/educ-annual-report-2024-2025.pdf)|214|[Government source](https://open.alberta.ca/dataset/8b226e68-1227-4aec-87a5-b573f3bfb062/resource/dcf58041-1aef-4f46-9452-b6a58f29d856/download/educ-annual-report-2024-2025.pdf)|
|Ministry AR Template Ma y 14, 2019|[health-2018-2019.pdf](../health/current/health-2018-2019.pdf)|139|[Government source](https://open.alberta.ca/dataset/4bb6bc99-ab59-47fd-a633-dfc27d7a049e/resource/32a0c20e-728d-4004-bc38-52f24ebd30cd/download/health-annual-report-2018-2019-web.pdf)|
|Alberta Health Annual Report 2019-2020|[health-2019-2020.pdf](../health/current/health-2019-2020.pdf)|169|[Government source](https://open.alberta.ca/dataset/4bb6bc99-ab59-47fd-a633-dfc27d7a049e/resource/04c7e15d-c88e-4172-b3fd-169be52ffe73/download/health-annual-report-2019-2020.pdf)|
|Health 2023-24 Annual Report|[health-2023-2024.pdf](../health/current/health-2023-2024.pdf)|162|[Government source](https://open.alberta.ca/dataset/4bb6bc99-ab59-47fd-a633-dfc27d7a049e/resource/0cbfe4d6-a288-4c51-91f6-7a0870de9b2c/download/hlth-annual-report-2023-2024.pdf)|
|Health Annual Report 2024-25|[hlth-annual-report-2024-2025.pdf](../health/current/hlth-annual-report-2024-2025.pdf)|164|[Government source](https://open.alberta.ca/dataset/4bb6bc99-ab59-47fd-a633-dfc27d7a049e/resource/6920038c-39c3-4dbd-ad36-14c649bff0a6/download/hlth-annual-report-2024-2025.pdf)|
|Affordability and Utilities Annual Report 2024-2025|[au-annual-report-2024-2025.pdf](../living_standards/au-annual-report-2024-2025.pdf)|89|[Government source](https://open.alberta.ca/dataset/ee6fc86b-2c20-4895-b677-9119712cd4e4/resource/bb863ea8-cfc3-473e-9df7-ef827308a9b7/download/au-annual-report-2024-2025.pdf)|
|Jobs, Economy and Trade Annual Report 2024-25|[jet-annual-report-2024-2025.pdf](../living_standards/jet-annual-report-2024-2025.pdf)|144|[Government source](https://open.alberta.ca/dataset/6dfd08a7-1e12-4b6b-b3c0-749d960f1143/resource/25d702f6-deca-46ed-a736-69522fcb0388/download/jet-annual-report-2024-2025.pdf)|
|Seniors, Community and Social Services 2024-25 Annual Report|[scss-annual-report-2024-2025.pdf](../living_standards/scss-annual-report-2024-2025.pdf)|133|[Government source](https://open.alberta.ca/dataset/3a6b50d8-c1f2-4e9a-94ec-62f1e0a34e59/resource/5b876aae-aaae-4c93-a9a1-4fe1305c7b39/download/scss-annual-report-2024-2025.pdf)|
|Annual Report - Government of Alberta 2024-2025|[goa-annual-report-2024-2025.pdf](../source_verification/downloads/goa-annual-report-2024-2025.pdf)|152|[Government source](https://open.alberta.ca/dataset/7714457c-7527-443a-a7db-dd8c1c8ead86/resource/e6c7f85c-73bc-44d3-af00-edebf01d82a1/download/goa-annual-report-2024-2025.pdf)|
|2024-25 Mental Health and Addiction Annual Report|[mha-annual-report-2024-2025.pdf](../source_verification/downloads/mha-annual-report-2024-2025.pdf)|133|[Government source](https://open.alberta.ca/dataset/610118c0-60ce-4ca1-9ef6-16fa703e46b7/resource/aa988084-3102-485c-97ff-3292b77e484c/download/mha-annual-report-2024-2025.pdf)|
|Public Safety and Emergency Services Annual Report 2024-2025|[pses-annual-report-2024-2025.pdf](../source_verification/downloads/pses-annual-report-2024-2025.pdf)|63|[Government source](https://open.alberta.ca/dataset/2b228e33-89ac-42d0-9c60-218d9ffb9f30/resource/0808ace0-ea4b-4139-bded-c100af68639d/download/pses-annual-report-2024-2025.pdf)|

## Statistics Canada poverty source

[Table11-10-0135-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110013501), Low income statistics by age, gender and economic family type. Release date2026-04-29 verified from the official table page; downloaded2026-10-09. The ZIP source, metadata, exact selected rows, vectors, quality flags and SHA256 are retained in [MBM_POVERTY.md](../living_standards/MBM_POVERTY.md). All-person estimates describe the survey-covered population; inaccessible additional survey metadata does not establish coverage of every resident. 2018-base and2023-base series are separate.

## Statistics Canada life-table source

[Table13-10-0837-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310083701), complete single-year life tables. Release date2026-01-13; retrieved2026-10-09. Age0/both-sexes Alberta andCanada estimates and source95% margins are retained separately. Metadata marks2023/2024 preliminary despite blank raw CSV status fields. [Life-table audit](../health/LIFE_EXPECTANCY_AUDIT.md) records definitions, metadata and independent official HTML-to-CSV comparison. These period estimates are not joined to archived AHCIP vintages.

## Archived financial source and claim trail

The main input panel uses supplied `Budget PDFs/2024-2025 Budget.pdf`, internally 2024–25 Final Results Year-End Report, PDF pp13–14. Its local source hash is included in the run manifest. The newly downloaded full2024–25 annual report independently repeats the historical fiscal table (physicalPDF14), including the6M discrepancy. Source publication dates differ from observed fiscal/calendar periods. Source-specific CSV ledgers retain exact page references, definitions, quotes and status. Published source labels/definitions are not accepted as semantic proof when they conflict with results.

## Delivery/runtime scope

No report-app preparer/runtime is callable in this execution environment; the shared Data runtime was unavailable in the preceding accepted workflow. Repository Markdown and an executed notebook with standalone figures remain the delivery path. No hosted report/site was published.
