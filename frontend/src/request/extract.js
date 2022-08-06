import request from "@/HttpCommon.js";

class ExtractApi {
  getExtracts(data) {
    return request.get("/api/extracts/list/", data);
  }

  getReportDetail(id) {
    return request.get("/api/reports/" + id + "/");
  }

  deleteReport(id) {
    return request.post("/api/reports/delete/" + id + "/");
  }
}

export default new ExtractApi();
