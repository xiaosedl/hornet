<template>
  <div class="project">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select v-model="projectForm.id" placeholder="选择项目">
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createTask">创建</el-button>
        </el-form-item>
      </el-form>

      <!--组件中，引入子组件-->
      <taskDialog
        v-if="dialogFlag"
        :pid="projectForm.id"
        :title="dialogTitle"
        @cancel="closeDialog"
      ></taskDialog>
    </div>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import taskDialog from "../../components/task/taskDialog.vue";

export default {
  name: "Project",
  components: {
    taskDialog,
  },
  data() {
    return {
      projectForm: {
        id: "",
      },
      projectOptions: [],
      dialogFlag: false,
      dialogTitle: "create",
      currentPorjectId: "",
      projectData: [],
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
    };
  },

  mounted() {
    // 加载 vue 组件同时获取项目列表
    console.log("pid--->", this.projectForm.id);
    this.initProjectList();
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      console.log("initProjectList--->", resp);
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
        this.$message.error("查询失败");
      }
    },

    // 展示弹窗
    createTask() {
      this.dialogTitle = "create";
      this.dialogFlag = true;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.initProjectList();
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.req.page = val;
      this.initProjectList();
    },

    // 弹出项目编辑弹出
    showEdit(id) {
      this.currentProjectId = id;
      this.dialogTitle = "edit";
      this.dialogFlag = true;
    },

    // 删除项目
    deleteProject(id) {
      console.log("delete", id);
      ProjectApi.deleteProject(id).then((resp) => {
        console.log("deleteProject", resp);
        if (resp.success === true) {
          this.$message.success("删除成功！");
          this.closeDialog();
        } else {
          this.$message.error("删除失败：" + resp.error.msg);
        }
      });
    },
  },
};
</script>
