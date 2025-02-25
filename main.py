from fastapi import FastAPI, Query
from search import search_by_query
from models import SearchResult, Container
import json

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the Exim Chatbot!"}

@app.post("/conversations", response_model=SearchResult)
def search(query: str = Query(..., description="Enter your search query")):
    result = search_by_query(query)


    if not result:
        return SearchResult(
            _id="N/A",
            job_number="N/A",
            year="N/A",
            assbl_value="N/A",
            awb_bl_date="N/A",
            awb_bl_no="N/A",
            be_date="N/A",
            be_no="N/A",
            bill_date="N/A",
            bill_no="N/A",
            cif_amount="N/A",
            consignment_type="N/A",
            container_count="0",
            containers=[],
            cth_no="N/A",
            custom_house="N/A",
            description="No matching record found.",
            exrate="N/A",
            gateway_igm="N/A",
            gateway_igm_date="N/A",
            gross_weight="N/A",
            igm_date="N/A",
            igm_no="N/A",
            voyage_no="N/A",
        )

    containers = result.get("container_nos", [])
    if not isinstance(containers, list):
        containers = []

    container_list = [
        Container(
            container_number=c.get("container_number", "N/A"),
            size=c.get("size", "N/A")  # Now extracting size
        )
        for c in containers
    ]



    return SearchResult(
        job_number=result.get("job_no", "N/A"),
        year=result.get("year", "N/A"),
        assbl_value=result.get("assbl_value", "N/A"),
        awb_bl_date=result.get("awb_bl_date", "N/A"),
        awb_bl_no=result.get("awb_bl_no", "N/A"),
        be_date=result.get("be_date", "N/A"),
        be_no=result.get("be_no", "N/A"),
        bill_date=result.get("bill_date", "N/A"),
        bill_no=result.get("bill_no", "N/A"),
        cif_amount=result.get("cif_amount", "N/A"),
        consignment_type=result.get("consignment_type", "N/A"),
        container_count=result.get("container_count", "N/A"),
        containers=container_list,
        cth_no=result.get("cth_no", "N/A"),
        custom_house=result.get("custom_house", "N/A"),
        description=result.get("description", "N/A"),
        exrate=result.get("exrate", "N/A"),
        gateway_igm=result.get("gateway_igm", "N/A"),
        gateway_igm_date=result.get("gateway_igm_date", "N/A"),
        gross_weight=result.get("gross_weight", "N/A"),
        igm_date=result.get("igm_date", "N/A"),
        igm_no=result.get("igm_no", "N/A"),
        voyage_no=result.get("voyage_no", "N/A"),
    )
