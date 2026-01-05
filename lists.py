import httpx
import mcp.server.fastmcp as fastmcp
import os
from dotenv import load_dotenv
from lists_util import get_salesforce_token
from pydantic import BaseModel, Field
from typing import Annotated
import mcp

load_dotenv()
lists_mcp = fastmcp.FastMCP("lists") 

async def get_list_metadata_helper(object_api_name, listview_api_name="", is_mru=False, is_search_result=False):

    token, instance_url = get_salesforce_token()
    # Use the id parameter in the endpoint
    if is_mru:
        url = f"{instance_url}/services/data/v64.0/ui-api/list-info/{object_api_name}/__Recent" 
    elif is_search_result:
        url = f"{instance_url}/services/data/v64.0/ui-api/list-info/{object_api_name}/__SearchResult"
    else:
        url = f"{instance_url}/services/data/v64.0/ui-api/list-info/{object_api_name}/{listview_api_name}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = httpx.get(url, headers=headers)
    return r.text



@lists_mcp.tool()
async def get_mru_metadata_by_obj_and_listview_id(object_api_name):
    """Get list mru metatdata given the obeject API name
    Args:
       object_api_name: Object API Name
    """

    return await get_list_metadata_helper(object_api_name=object_api_name, is_mru=True, is_search_result=False)



@lists_mcp.tool()
async def get_metadata_by_obj_and_listview_id(object_api_name, listview_api_name):
    """Get list metatdata given the obeject API name and listview API name
    Args:
       object_api_name: Object API Name
       listview_api_name: Listview API Name
    """

    return await get_list_metadata_helper(object_api_name=object_api_name, listview_api_name=listview_api_name, is_mru=False, is_search_result=False)


@lists_mcp.tool()
async def get_search_result_metadata_by_obj_and_listview_id(object_api_name):
    """Get list search result metatdata given the obeject API name
    Args:
       object_api_name: Object API Name
    """

    return await get_list_metadata_helper(object_api_name=object_api_name, is_mru=False, is_search_result=True)



# @lists_mcp.prompt()
# def get_list_info(id: str) -> str:
#     return f"Please get the list info for the list with the id: {id}"


# @lists_mcp.resource("config://app")
# def get_config() -> str:
#     """Static configuration data"""
#     return "App configuration here"


# @lists_mcp.resource("users://{user_id}/profile")
# def get_user_profile(user_id: str) -> str:
#     """Dynamic user data"""
#     return f"Profile data for user {user_id}"


if __name__ == "__main__":
    lists_mcp.run(transport="stdio")