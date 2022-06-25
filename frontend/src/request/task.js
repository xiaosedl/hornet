import request from "@/HttpCommon.js";

class TaskApi {
  getTasks(data) {
    return request.get("/api/tasks/list/", data);
  }

  getTaskDetail(id) {
    return request.get("/api/tasks/" + id + "/");
  }

  createTask(data) {
    return request.post("/api/tasks/", data);
  }

  updateTask(id, data) {
    return request.put("/api/tasks/update/" + id + "/", data);
  }

  deleteTask(id) {
    return request.delete("/api/tasks/delete/" + id + "/");
  }

  runningTask(id) {
    return request.post("/api/tasks/" + id + "/running/");
  }
}

export default new TaskApi();
