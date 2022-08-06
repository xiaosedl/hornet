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
        <el-form-item label="任务描述">
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
            <div
              style="width: 100%; float: right; text-align: right; margin: 10px"
            >
              <el-pagination
                @current-change="handleCurrentChange"
                background
                layout="prev, pager, next"
                :page-size="req.size"
                :total="total"
              >
              </el-pagination>
            </div>
          </div>
        </el-form-item>
        <el-form-item style="text-align: right">
          <div class="dialog-footer">
            已选择【{{ this.caseNum }}】条用例
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" @click="submitForm('ruleForm')"
              >保存</el-button
            >
          </div>
        </el-form-item>
      </div>
    </el-form>
  </el-dialog>
</template>

<script>
import TaskApi from "../../request/task";
import ModuleApi from "../../request/module";

export default {
  name: "taskDialog",
  props: ["title", "pid", "tid"],
  data() {
    return {
      showTitle: "",
      dialogVisible: true,
      taskForm: {
        project: this.pid,
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
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
    };
  },
  mounted() {
    this.initModuleList();

    if (this.title === "create") {
      this.showTitle = "创建任务";
    } else if (this.title === "edit") {
      this.showTitle = "编辑任务";
    }
  },
  methods: {
    // 关闭弹窗
    closeDialog() {
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },

    // 点击了模块节点
    nodeClick(data) {
      this.req.page = 1;
      this.currentModuleId = data.id;
      this.getModuleCaseList(data.id);
    },

    // 查询模块列表，树形结构
    async initModuleList() {
      const req = { project_id: this.pid };
      const resp = await ModuleApi.getModuleTree(req);
      if (resp.success === true) {
        this.moduleData = resp.items;
        if (this.title === "edit") {
          await this.getTaskDetail();
        }
      } else {
        this.$message.error("查询失败");
      }
    },

    // 查看任务详情
    async getTaskDetail() {
      const resp = await TaskApi.getTaskDetail(this.tid);
      if (resp.success === true) {
        this.taskForm = resp.item;
        this.calculationCase();
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 选择一条用例
    selectionOneCases(val) {
      this.selectiveCase(val);
    },

    // 选择所有用例
    selectionAllCases(val) {
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
      const resp = await ModuleApi.getModuleCases(mid, this.req);
      if (resp.success === true) {
        this.caseData = resp.items;
        this.total = resp.total;

        // 已经选择的用例
        this.$nextTick(() => {
          let casesId = [];
          for (let i = 0; i < this.taskForm.cases.length; i++) {
            if (this.taskForm.cases[i].moduleId === mid) {
              casesId = this.taskForm.cases[i].casesId;
            }
          }

          let rows = [];
          for (let i = 0; i < casesId.length; i++) {
            for (let j = 0; j < this.caseData.length; j++) {
              if (casesId[i] === this.caseData[j].id) {
                rows.push(this.caseData[j]);
              }
            }
          }

          rows.forEach((row) => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        });
      } else {
        this.$message.error(resp.error.message);
      }
    },

    // 公共方法
    selectiveCase(multipleSelection) {
      const moduleCases = [];
      for (let i = 0; i < multipleSelection.length; i++) {
        moduleCases.push(multipleSelection[i].id);
      }

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
      this.calculationCase();
    },

    // 创建/编辑项目弹窗，请求创建/编辑项目接口
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.title === "create") {
            TaskApi.createTask(this.taskForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog();
              } else {
                this.$message.error(resp.error.msg);
              }
            });
          } else if (this.title === "edit") {
            TaskApi.updateTask(this.tid, this.taskForm).then((resp) => {
              if (resp.success === true) {
                this.closeDialog();
              } else {
                this.$message.error(resp.error.msg);
              }
            });
          }
        } else {
          return false;
        }
      });
    },

    // 初始化用例
    async initCaseList(mid) {
      const resp = await ModuleApi.getModuleCases(mid, this.req);
      if (resp.success === true) {
        this.caseData = resp.items;
        this.total = resp.total;
        this.$message.success("查询用例成功");
      } else {
        this.$message.error(resp.error.mag);
      }
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val;
      this.getModuleCaseList(this.currentModuleId);
    },
  },
};
</script>
