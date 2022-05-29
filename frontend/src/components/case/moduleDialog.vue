<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="500px"
    :before-close="closeDialog"
  >
    <el-form
      :model="moduleForm"
      :rules="rules"
      ref="projectForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="项目" prop="name">
        <el-input v-model="projectLabel" disabled></el-input>
      </el-form-item>
      <el-form-item label="父节点" v-if="rootFlag !== 1">
        <el-input v-model="parentObj.label" disabled></el-input>
      </el-form-item>
      <el-form-item label="模块名称" prop="name">
        <el-input v-model="moduleForm.name"></el-input>
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
import ModuleApi from "../../request/module";

export default {
  name: "Dialog",
  props: ["title", "projectId", "rootFlag", "projectLabel", "parentObj"],
  projectData: [],
  data() {
    return {
      dialogVisible: true,
      disable: false,
      showTitle: "",
      moduleForm: {
        name: "",
        project_id: 0,
        parent_id: 0,
      },
      rules: {
        name: [
          { required: true, message: "请输入名称", trigger: "blur" },
          {
            min: 1,
            max: 50,
            message: "长度在 1 到 50 个字符",
            trigger: "blur",
          },
        ],
      },
    };
  },
  mounted() {
    this.moduleForm.project_id = this.projectId;
    if (this.rootFlag === 1) {
      this.showTitle = "创建根节点";
    } else {
      this.showTitle = "创建子节点";
      this.moduleForm.parent_id = this.parentObj.id;
    }
  },
  methods: {
    // 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },

    // 创建模块
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          ModuleApi.createModule(this.moduleForm).then((resp) => {
            console.log("createProject", resp);
            if (resp.success === true) {
              this.$message.success("创建成功！");
              this.closeDialog();
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
};
</script>

<style scoped></style>
