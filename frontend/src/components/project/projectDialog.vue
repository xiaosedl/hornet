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
      <el-form-item label="图片" prop="desc">
        <div id="image">
          <el-upload
            action="#"
            :before-upload="beforeUpload"
            list-type="picture-card"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="imageVisible">
            <img width="100%" :src="imageUrl" alt="" />
          </el-dialog>
        </div>
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
      imageUrl: "",
      imageVisible: false,
      dialogVisible: true,
      fileList: [],
      disable: false,
      showTitle: "",
      projectForm: {
        name: "",
        desc: "",
        image: "",
      },
      rules: {
        name: [
          { required: true, message: "请输入项目名称", trigger: "blur" },
          {
            min: 1,
            max: 50,
            message: "长度在 1 到 50 个字符",
            trigger: "blur",
          },
        ],
        desc: [{ required: false, message: "请填写项目描述", trigger: "blur" }],
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
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },

    // 项目编辑弹窗获取项目详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid);
      if (resp.success === true) {
        this.projectForm = resp.item;
        this.fileList.push({
          name: this.projectForm.image,
          url: "/static/images/" + resp.item.image,
        });
        this.$message.success("查询项目详情成功！");
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
          this.$message.error("保存失败");
          return false;
        }
      });
    },

    // 删除图片
    handleRemove(file) {
      this.fileList.remove(file);
    },

    // 预览图片
    handlePreview(file) {
      this.imageUrl = file.url;
      this.imageVisible = true;
    },

    // 上传图片
    beforeUpload(file) {
      let fd = new FormData();
      fd.append("file", file);

      ProjectApi.uploadImage(fd).then((resp) => {
        if (resp.data.success === true) {
          this.projectForm.image = resp.data.item;
          const imagePath = "/static/images/" + resp.data.item;

          this.fileList.push({
            name: file.name,
            url: imagePath,
          });
          this.$message.success("上传成功");
        } else {
          this.$message.error(resp.data.error.message);
        }
      });
      return true;
    },
  },
};
</script>

<style scoped>
#image {
  text-align: left;
}
</style>
