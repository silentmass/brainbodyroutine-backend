from fastapi import APIRouter


router_aws = APIRouter(prefix="/api/aws", tags=["Aws"])


@router_aws.get("/search")
async def search_products():
    print("At AWS")
    return {"Hello": "AWS"}
