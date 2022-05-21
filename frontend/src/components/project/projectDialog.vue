<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      :model="projectForm"
      :rules="rules"
      ref="projectForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目名称" prop="name">
        <el-input v-model="projectForm.name"></el-input>
      </el-form-item>
      <el-form-item label="项目描述" prop="describe">
        <el-input type="textarea" v-model="projectForm.describe"></el-input>
      </el-form-item>
      <el-form-item style="text-align: right">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="submitForm('projectForm')"
          >确定</el-button
        >
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
import ProjectApi from "../../request/project";

export default {
  name: "Dialog",
  props: ["title", "pid"],
  projectData: [],
  data() {
    return {
      imgUploadUrl: "http://127.0.0.1:8000/api/projucts/upload",
      dialogVisible: true,
      showTitle: "",
      projectForm: {
        name: "",
        desc: "",
        image: "e4df4540c6d1861b09bdc5bcb1b312ef.jpg",
      },
      rules: {
        name: [
          { required: true, message: "请输入活动名称", trigger: "blur" },
          {
            min: 1,
            max: 50,
            message: "长度在 1 到 50 个字符",
            trigger: "blur",
          },
        ],
        desc: [{ required: false, message: "请填写活动形式", trigger: "blur" }],
      },
    };
  },
  mounted() {
    if (this.title === "create") {
      this.showTitle = "创建项目";
    } else if (this.title === "edit") {
      this.showTitle = "编辑项目";
      this.initProject();
    }
  },
  methods: {
    // 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },

    // 项目编辑弹窗获取项目详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid);
      console.log("--->", resp);
      if (resp.success === true) {
        this.projectForm = resp.item;
        this.$message.success("查询项目详情成功！");
        console.log("----->", resp.total);
      } else {
        this.$message.error("查询项目详情失败");
      }
    },

    // 创建/编辑项目弹窗，请求创建/编辑项目接口
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === "create") {
            ProjectApi.createProject(this.projectForm).then((resp) => {
              console.log("createProject", resp);
              if (resp.success === true) {
                this.$message.success("创建成功！");
                this.closeDialog();
              } else {
                this.$message.error(resp.error.msg);
              }
            });
          } else if (this.title === "edit") {
            ProjectApi.updateProject(this.pid, this.projectForm).then(
              (resp) => {
                console.log("updateProject", resp);
                if (resp.success === true) {
                  this.$message.success("编辑成功！");
                  this.closeDialog();
                } else {
                  this.$message.error(resp.error.msg);
                }
              }
            );
          }
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
};
</script>
