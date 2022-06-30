<template>
  <div class="task">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select
            v-model="projectForm.id"
            placeholder="选择项目"
            @change="changeProject"
          >
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item style="float: right">
          <el-button type="primary" @click="createTask">创建</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-table
        :data="taskData"
        border
        header-align="center"
        style="width: 100%; margin: 10px 0"
      >
        <el-table-column prop="id" label="ID" width="60%" align="center">
        </el-table-column>
        <el-table-column
          prop="name"
          label="任务名称"
          width="224%"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="describe"
          label="项目描述"
          width="300%"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="update_time"
          label="更新时间"
          width="250%"
          header-align="center"
        >
        </el-table-column>
        <el-table-column prop="status" label="状态" width="150%" align="center">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-tag type="info">未执行</el-tag>
            </div>
            <div v-else-if="scope.row.status === 1">
              <el-tag type="success">执行中</el-tag>
            </div>
            <div v-else-if="scope.row.status === 2">
              <el-tag>已执行</el-tag>
            </div>
            <div v-else>
              <el-tag type="danger">未知状态</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="操作" width="150%" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="runTask(scope.row)"
              >执行</el-button
            >
            <el-button type="text" size="small" @click="clickEdit(scope.row)"
              >编辑</el-button
            >
            <el-button type="text" size="small" @click="deleteTask(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 100%; float: right; text-align: right; margin: 10px">
      <el-pagination
        @current-change="handleCurrentChange"
        background
        layout="prev, pager, next"
        :page-size="req.size"
        :total="total"
      >
      </el-pagination>
    </div>
    <!--组件中，引入子组件-->
    <taskDialog
      v-if="dialogFlag"
      :pid="projectForm.id"
      :tid="taskId"
      :title="dialogTitle"
      @cancel="closeDialog"
    ></taskDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import taskDialog from "../../components/task/taskDialog.vue";
import TaskApi from "../../request/task";

export default {
  name: "Task",
  components: {
    taskDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      projectOptions: [],
      dialogFlag: false,
      dialogTitle: "create",
      currentProjectId: "",
      taskId: "",
      projectData: [],
      moduleData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
      taskData: [],
      taskHeartbeat: null,
    };
  },

  created() {
    // 加载 vue 组件同时获取项目列表
    this.initProjectList();
  },

  mounted() {
    // 任务列表的心跳，5s请求一次
    this.taskHeartbeat = setInterval(() => {
      this.initTaskList();
    }, 5000);
  },

  destroyed() {
    // 组件退出时销毁心跳
    clearInterval(this.taskHeartbeat);
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      if (resp.success === true) {
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;

        for (let i = 0; i < resp.items.length; i++) {
          this.projectOptions.push({
            value: resp.items[i].id,
            label: resp.items[i].name,
          });
        }
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 修改选中的项目
    changeProject(value) {
      this.projectForm.id = value;
      this.initTaskList();
    },

    // 初始化任务列表
    async initTaskList() {
      const req = {
        project_id: this.projectForm.id,
        page: this.req.page,
        size: this.req.size,
      };
      const resp = await TaskApi.getTasks(req);
      if (resp.success === true) {
        console.log("tasks", resp);
        this.taskData = resp.items;
        this.total = resp.total;
      } else {
        this.$message.error(resp.error.mag);
      }
    },

    // 编辑任务
    clickEdit(row) {
      this.dialogTitle = "edit";
      this.taskId = row.id;
      this.dialogFlag = true;
    },

    // 展示弹窗
    createTask() {
      this.dialogTitle = "create";
      this.dialogFlag = true;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.initTaskList();
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val;
      this.initTaskList();
    },

    // 弹出项目编辑弹出
    showEdit(id) {
      this.currentProjectId = id;
      this.dialogTitle = "edit";
      this.dialogFlag = true;
    },

    // 删除任务
    async deleteTask(row) {
      console.log("delete--->", row.id);
      const resp = await TaskApi.deleteTask(row.id);
      if (resp.success === true) {
        this.closeDialog();
      } else {
        this.$message.error("删除失败：" + resp.error.msg);
      }
    },

    // 执行任务
    async runTask(row) {
      const resp = await TaskApi.runningTask(row.id);
      if (resp.success === true) {
        this.$message.success("开始执行");
        this.closeDialog();
      } else {
        this.$message.error(resp.error.msg);
      }
    },
  },
};
</script>
