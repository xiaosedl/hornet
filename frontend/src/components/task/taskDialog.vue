<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <el-form
      :model="taskForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <div>
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name"></el-input>
        </el-form-item>
        <el-form-item label="任务描述" prop="describe">
          <el-input type="textarea" v-model="taskForm.describe"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="block">
            <el-card style="width: 30%; margin: 20px 0; float: left">
              <el-tree
                :data="moduleData"
                node-key="id"
                default-expand-all
                :expand-on-click-node="false"
                @node-click="nodeClick"
              >
              </el-tree>
            </el-card>
            <div style="width: 67%; margin: 20px 0; float: right">
              <el-table
                ref="multipleTable"
                :data="caseData"
                border
                header-align="center"
                @select-all="selectionAllCases"
                @select="selectionOneCases"
              >
                <el-table-column type="selection" width="55"> </el-table-column>
                <el-table-column prop="id" label="ID" header-align="center">
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="名称"
                  header-align="center"
                ></el-table-column>
              </el-table>
            </div>
          </div>
        </el-form-item>
        <el-form-item style="text-align: right">
          <div class="dialog-footer">
            已选择【{{ this.caseNum }}】条用例
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" @click="submitForm('taskForm')"
              >确定</el-button
            >
          </div>
        </el-form-item>
      </div>
    </el-form>
  </el-dialog>
</template>

<script>
import ProjectApi from "../../request/project";
import ModuleApi from "../../request/module";

export default {
  name: "taskDialog",
  props: ["title", "pid"],
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      taskForm: {
        name: "",
        describe: "",
        cases: [],
      },
      rules: {
        name: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
      },
      moduleData: [],
      caseData: [],
      currentModuleId: 0,
      caseNum: 0,
    };
  },
  mounted() {
    this.initModuleList();

    if (this.title === "create") {
      this.showTitle = "创建任务";
    } else if (this.title === "edit") {
      this.showTitle = "编辑任务";
      this.initProject();
    }
  },
  methods: {
    // 点击了模块节点
    nodeClick(data) {
      console.log("点击了节点", data);
      this.currentModuleId = data.id;
      this.getModuleCaseList(data.id)
    },


    // 查询模块列表，树形结构
    async initModuleList() {
      const req = { project_id: this.pid };
      const resp = await ModuleApi.getModuleTree(req);
      console.log("getModules--->", resp.items);
      if (resp.success === true) {
        this.moduleData = resp.items;
      } else {
        this.$message.error("查询失败");
      }
    },

    // 选择一条用例
    selectionOneCases(val, row) {
      console.log("选择一条用例 val--->", val);
      console.log("选择一条用例 row--->", row);
      this.selectiveCase(val);
    },

    // 选择所有用例
    selectionAllCases(val) {
      console.log("val", val);
      this.selectiveCase(val);
    },

    // 公共方法，计算用例的数量
    calculationCase() {
      this.caseNum = 0;
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        this.caseNum += this.taskForm.cases[i].casesId.length;
      }
    },

    // 初始化用例数据，记住选择过的用例
    async getModuleCaseList(mid) {

      const resp = await ModuleApi.getModuleCases(mid)
      if (resp.success === true) {
        this.caseData = resp.items

        // 已经选择的用例
        this.$nextTick(() => {
          let casesId = []
          for (let i = 0; i < this.taskForm.cases.length; i++) {
            if (this.taskForm.cases[i].moduleId === mid) {
              casesId = this.taskForm.cases[i].casesId
            }
          }

          let rows = []
          for (let i = 0; i < casesId.length; i++) {
            for (let j = 0; j < this.caseData.length; j++) {
              if (casesId[i] === this.caseData[j].id) {
                rows.push(this.caseData[j])
              }
            }
          }

          rows.forEach((row) => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        })
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 公共方法
    selectiveCase(multipleSelection) {
      const moduleCases = [];
      for (let i = 0; i < multipleSelection.length; i++) {
        moduleCases.push(multipleSelection[i].id);
      }

      console.log("选择的用例--->", moduleCases);

      let selective = false;
      for (let i = 0; i < this.taskForm.cases.length; i++) {
        if (this.taskForm.cases[i].moduleId === this.currentModuleId) {
          selective = true;
          this.taskForm.cases[i].casesId = moduleCases;
        }
      }

      if (selective === false) {
        this.taskForm.cases.push({
          moduleId: this.currentModuleId,
          casesId: moduleCases,
        });
      }
      console.log("taskForm case", this.taskForm.cases);
      this.calculationCase();
    },

    // 关闭弹窗
    closeDialog() {
      console.log("closeDialog");
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },

    // 任务编辑弹窗获取任务详情
    async initProject() {
      const resp = await ProjectApi.getProject(this.pid);
      console.log("--->", resp);
      if (resp.success === true) {
        this.taskForm = resp.item;
        this.fileList.push({
          name: this.taskForm.image,
          url: "/static/images/" + resp.item.image,
        });
        this.$message.success("查询任务详情成功！");
        console.log("----->", resp.total);
      } else {
        this.$message.error("查询任务详情失败");
      }
    },

    // 创建/编辑项目弹窗，请求创建/编辑项目接口
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === "create") {
            ProjectApi.createProject(this.taskForm).then((resp) => {
              console.log("createProject", resp);
              if (resp.success === true) {
                this.$message.success("创建成功！");
                this.closeDialog();
              } else {
                this.$message.error(resp.error.msg);
              }
            });
          } else if (this.title === "edit") {
            ProjectApi.updateProject(this.pid, this.taskForm).then((resp) => {
              console.log("updateProject", resp);
              if (resp.success === true) {
                this.$message.success("编辑成功！");
                this.closeDialog();
              } else {
                this.$message.error(resp.error.msg);
              }
            });
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

<style scoped>
#image {
  text-align: left;
}
</style>
