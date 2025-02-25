from pydantic import BaseModel
from typing import List, Optional

class Container(BaseModel):
    container_number: str
    size: Optional[str] = None

class SearchResult(BaseModel):
    job_number: str
    year: str
    assbl_value: str
    awb_bl_date: str
    awb_bl_no: str
    be_date: str
    be_no: str
    bill_date: str
    bill_no: str
    cif_amount: str
    consignment_type: str
    container_count: Optional[str]
    containers: Optional[List[Container]]
    cth_no: str
    custom_house: str
    description: str
    exrate: str
    gateway_igm: str
    gateway_igm_date: str
    gross_weight: str
    igm_date: str
    igm_no: str
    voyage_no: str