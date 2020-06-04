USE SCRATCH

UPDATE [KG_CORPORATEBOUNDARYLOAD]
set [URBANCITYNAME] = 'Rural' WHERE [URBANCITYNAME] = ''

UPDATE [KG_CORPORATEBOUNDARYLOAD]
set [URBANCITYNO] = '999' WHERE [URBANCITYNO] = '0'

UPDATE [KG_CORPORATEBOUNDARYLOAD]
set [URBANCITYNO] = '999' WHERE [URBANCITYNO] = '99999'

UPDATE [KG_CORPORATEBOUNDARYLOAD]
set [hpms_urban_code] = '99999' where [hpms_urban_code] = ''

select
ROW_NUMBER() OVER(ORDER BY a.routeid, fmeas ASC) AS Rownum,
CONCAT('BoundaryEvent_', ROW_NUMBER() OVER(ORDER BY a.routeid, fmeas ASC)) EVENTID,
a.routeid,
fmeas frommeasure,
tmeas tomeasure,
case when hpms_urban_code = '' THEN '99999' ELSE hpms_urban_code END urbanareacode,
urbancityno urbanjurisdiction,
cast(fhwa_approved as datetime) InventoryStartDate,
cast(b.lrsfromdate as datetime) lrsfromdate,
cast(NULL as datetime) lrstodate,
'ASD' SourceCIT
into scratch.tdsuser.kg_UrbJur018
from scratch.tdsuser.[KG_CORPORATEBOUNDARYLOAD] a
left join khub.rh.lrs_county b
on a.routeid = b.routeid
where substring(a.routeid,4,1) = '6'
and b.lrstodate is null
