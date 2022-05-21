import request from "@/HttpCommon.js";

class ProjectApi {
  getProjects(data) {
    return request.get("/api/projects/list/", data);
  }

  getProject(id) {
    return request.get("/api/projects/" + id + "/");
  }

  createProject(data) {
    return request.post("/api/projects/", data);
  }

  updateProject(id, data) {
    return request.put("/api/projects/update/" + id + "/", data);
  }

  deleteProject(id) {
    return request.delete("/api/projects/delete/" + id + "/");
  }
}

export default new ProjectApi();
