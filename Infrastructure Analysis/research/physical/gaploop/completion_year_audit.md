# Completed status is not necessarily a newly completed event

The 17-row initial timeline is preserved as a work-history artifact in `round2/`. **Use `gaploop/project_timeline_audited.csv` or JSON for event-year-sensitive work.** The initial `construction_completion_fy` field mixed completed-status observation dates with actual dated completions. The audited table distinguishes these cases explicitly and does not discard prior source evidence.

## Direct counterexample

**Quest Project—Scotford Upgrader appears in the 2021–22 completed-project map(page 19) and description(page 23). However, 2016–17 PDF p. 17 explicitly says 2016–17 was “the Quest project's first full year of injections.”** The 2021–22 list therefore cannot be treated as evidence that this asset first became physically complete or operational in 2021–22. That list includes projects already operating earlier whose funding/closeout record remains relevant. This differs from school lists that expressly say “the following…projects were completed in 2024–25”, although even those can include planning entries in earlier years.

The 2021–22 footer says projects are completed when operational; 2022–23 onwards says construction ended and pre-operational support can continue. Both describe status definitions, **not a guarantee that every listed project's first completion event fell within that reporting year**. The source itself provides an “as of March 31” umbrella in its project section.

## What changed in the audit

- `first_reported_completed_status_fy`: first completed-status observation recovered in this limited local corpus. This is not necessarily the first report ever published or the actual completion event.
- `explicit_construction_completion_fy`: populated only when the recovered passage itself dates the event or the named school list explicitly dates its completions.
- `explicit_calendar_completion_date`: populated only for explicitly dated source statements.
- `operational_year_if_verified`: remains null except Anthony Henday 2016, for which the P3 schedule explicitly identifies an already operational asset.
- `prior_ledger_claimed_completion_fy`: preserved for transparent audit history; do not use as an event date.

**Four of 17 selected records support an explicitly dated construction completion fiscal year:** Anthony Henday 2016–17, Highway 63 (2016–17), St Veronica school 2019–20, Elder Dr Francis Whiskeyjack 2024–25. The other 13 support as of-status observations and physical descriptions without independently dated handover events. Earlier ongoing versus later completed status may bracket a transition but should not be silently converted into an exact date, especially for phases and changed completion definitions.

## Additional dated operational evidence

2016–17 PDF p. 72 P3 schedule labels the Northeast Anthony Henday contract among projects “already operational”, giving a completion date September 2016 and capital payments beginning October 2016. The narrative p. 21 says Anthony Henday completed October 2016. These support operational calendar year 2016; the different monthly milestones should remain distinct rather than asserting a unique day/month handover. The 2015–16 P3 table p. 67 still identified the Northeast contract under construction, contracted May 2012.

## Additional source examples

2021–22 completed map p. 19 and description p. 23 include **Southwest Calgary Ring Road 31 km**, while the West Calgary Ring Road remains ongoing on p. 19. The final west/whole-ring completed status is 2023–24 p. 23. Treat these as stages within one ring program, not independent entire ring additions.

The 2021–22 description claims 31 km is about 20% of the entire ring, but the later whole-ring figure is 101 km, making 31/101≈30.7%. **Do not repeat the 20% share** or combine the figures into a supposedly consistent segment decomposition without reconciliation. Absolute 31 km and 101 km belong to their respective quoted descriptions.

2021–22 completed map also includes the **Bragg Creek Flood Mitigation Project**; p. 23 describes berm construction and replacement of an undersized Elbow River bridge. This is a second verified local flood-resilience project, distinct from Springbank. Replacement is not a net new bridge and the source lacks a measured damage-avoidance outcome or an exact first operation date.

## Isolated map-stage ambiguity

Visual inspection of 2020–21 PDF p. 20 puts **Provincial Pharmacy Central Drug Production and Distribution Centre** among province-wide projects on the completed side. Its detailed p. 22 entry instead gives expected completion Fall 2024, and 2021–22 p. 19/2022–23 p. 19/2024–25 p. 19 classify the centre ongoing. This could reflect an editorial/map classification or unidentified phase/scope difference; the sources do not resolve it. Do not assign a completed status to the whole centre from the isolated 2020 map. Rendered source maps are saved in `gaploop/map2020-21_pdf-page20.png`, `map2021-22_pdf-page19.png`, and `map2022-23_pdf-page19.png`.

The 2019–20 map/p. 17 is also image-heavy and shows University of Lethbridge Destination on completed side; the description p. 19 separately gives the explicit date **“Completed January 2020”**. That supports an actual fiscal 2019–20 completion date, unlike most general list observations. The 2022–23 map/p. 19 and description p. 23 show University of Calgary MacKimmie redevelopment completed status and an unquantified student-capacity increase. These are usable post-secondary examples with different date precision, not standardized campus-seats metrics.
