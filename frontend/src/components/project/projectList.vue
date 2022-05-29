<template>
  <div class="project">
    <div style="text-align: left">
      <el-button type="primary" style="height: 50px" @click="showDialog"
        >创建</el-button
      >
    </div>
    <div v-for="(item, index) in projectData" :key="index" class="item">
      <el-col :span="7" class="project-card">
        <el-card>
          <div slot="header" class="clearfix">
            <span>{{ item.name }}</span>
            <div style="float: right">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <i class="el-icon-setting"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="edit">
                    <el-button type="text" @click="showEdit(item.id)"
                      >编辑</el-button
                    >
                  </el-dropdown-item>
                  <el-dropdown-item command="delete">
                    <el-button type="text" @click="deleteProject(item.id)"
                      >删除</el-button
                    >
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
          <div style="height: 30px">
            {{ item.describe }}
          </div>
          <div style="margin: 5px">
            <img
              :src="item.image"
              class="image"
              style="width: 200px; height: 200px"
            />
          </div>
        </el-card>
      </el-col>
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
    <projectDialog
      v-if="dialogFlag"
      :pid="currentProjectId"
      :title="dialogTitle"
      @cancel="closeDialog"
    ></projectDialog>
  </div>
</template>

<style>
.project-card {
  float: right;
  width: 31%;
  height: 40%;
  margin: 10px;
}
</style>

<script>
import projectDialog from "../../components/project/projectDialog.vue";
import ProjectApi from "../../request/project";

export default {
  name: "Project",
  components: {
    projectDialog,
  },
  data() {
    return {
      dialogFlag: false,
      dialogTitle: "create",
      currentProjectId: "",
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
    this.initProjectList();
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      console.log("--->", resp);
      if (resp.success === true) {
        // 处理图片访问路径
        for (let i = 0; i < resp.items.length; i++) {
          resp.items[i].image = "/static/images/" + resp.items[i].image;
        }

        this.projectData = resp.items;
        this.total = resp.total;
        this.$message.success("查询成功！");
        console.log("----->", resp.total);
      } else {
        this.$message.error("查询失败");
      }
    },

    // 展示弹窗
    showDialog() {
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
