import request from "@/HttpCommon.js";

class ReportApi {
  getReports(data) {
    return request.get("/api/reports/list/", data);
  }

  getReportDetail(id) {
    return request.get("/api/reports/" + id + "/");
  }

  deleteReport(id) {
    return request.post("/api/reports/delete/" + id + "/");
  }
}

export default new ReportApi();
