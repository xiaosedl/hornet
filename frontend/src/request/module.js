import request from "@/HttpCommon.js";

class ModuleApi {
  getModuleTree(data) {
    return request.get("/api/modules/tree", data);
  }

  getModuleCases(mid, data) {
    return request.get("/api/modules/" + mid + "/cases/", data);
  }

  createModule(data) {
    return request.post("/api/modules/", data);
  }

  deleteModule(mid) {
    return request.delete("/api/modules/delete/" + mid);
  }
}

export default new ModuleApi();
