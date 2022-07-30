<template>
  <div class="case">
    <div style="text-align: left">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select
            v-model="projectValue"
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
          <el-button type="primary" @click="caseCreate">创建</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="block">
      <el-card style="width: 28%; margin: 20px 0; float: left">
        <el-button
          type="text"
          icon="el-icon-circle-plus-outline"
          @click="createRootDialog"
          >根节点</el-button
        >
        <el-tree
          v-model="projectValue"
          :data="moduleData"
          show-checkbox
          node-key="id"
          :default-expand-all="true"
          :expand-on-click-node="false"
          :highlight-current="true"
          @node-click="nodeClick"
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button type="text" size="mini" @click="() => remove(data)">
                <i class="el-icon-remove-outline"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
      <el-table
        :data="caseData"
        border
        @row-click="caseRowClick"
        header-align="center"
        style="width: 70%; margin: 20px 0; float: right"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="50px"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="name"
          label="名称"
          width="180px"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="method"
          label="请求方法"
          width="80px"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="url"
          label="请求地址"
          width="200px"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="module.name"
          label="模块名称"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          width="180"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="update_time"
          label="更新时间"
          width="180"
          header-align="center"
        >
        </el-table-column>
      </el-table>
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
    </div>

    <el-drawer
      :title="caseTitle"
      v-model="drawer"
      :visible.sync="drawer"
      direction="rtl"
      size="50%"
    >
      <!--引入用例抽屉子组件-->
      <caseDialog
        v-if="drawer"
        :mid="currentModule"
        :cid="currentCase"
        :drawerFlag="drawer"
        :caseTitle="caseTitle"
      ></caseDialog>
    </el-drawer>

    <!--引入模块弹窗子组件-->
    <moduleDialog
      v-if="dialogFlag"
      :projectId="projectValue"
      :projectLabel="projectLabel"
      :parentObj="parentObj"
      :rootFlag="rootFlag"
      @cancel="closeDialog"
    ></moduleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import ModuleApi from "../../request/module";
import moduleDialog from "./moduleDialog";
import caseDialog from "./caseDialog";

export default {
  name: "caseModule",
  components: {
    moduleDialog,
    caseDialog,
  },
  data() {
    return {
      projectOptions: [],
      projectValue: 1,
      projectLabel: "",
      moduleData: [],
      rootFlag: 1,
      dialogFlag: false,
      currentProjectId: "",
      parentObj: {},
      caseData: [],
      drawer: false,
      caseTitle: "",
      currentModule: 0, // 当前选中的模块
      currentCase: 0, // 当前选中的用例
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
    };
  },

  mounted() {
    // 加载 vue 组件同时初始化模块列表

    this.initModuleList(this.projectValue);
    this.initProjectList();
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
        this.$message.error("查询失败");
      }
    },

    // 修改选中的项目
    changeProject(value) {
      this.projectValue = value;
      this.projectLabel = this.projectOptions.find(
        (item) => item.value === value
      ).label;
      this.initModuleList(value);
    },

    // 查询模块列表，树形结构
    async initModuleList(projectId) {
      const req = { project_id: projectId };
      const resp = await ModuleApi.getModuleTree(req);
      if (resp.success === true) {
        this.moduleData = resp.items;
      } else {
        this.$message.error("查询失败");
      }
    },

    // 创建子节点
    append(data) {
      this.dialogFlag = true;
      this.rootFlag = false;
      this.parentObj = data;
    },

    // 删除节点
    remove(data) {
      ModuleApi.deleteModule(data.id).then((resp) => {
        if (resp.success === true) {
          this.$message.success("删除成功！");
          this.initModuleList(this.projectValue);
        } else {
          this.$message.error(resp.error.msg);
        }
      });
    },

    // 创建根节点弹窗
    createRootDialog() {
      this.dialogFlag = true;
      this.rootFlag = 1;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.parentObj = {};
      this.initModuleList(this.projectValue);
    },

    // 点击了模块节点
    nodeClick(data) {
      this.req.page = 1;
      this.currentModule = data.id;
      this.initCaseList(data.id);
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

    // 点击用例，弹出抽屉，查看用例
    caseRowClick(row) {
      this.currentCase = row.id;
      this.drawer = true;
      this.caseTitle = "查看用例";
    },

    // 创建用例
    caseCreate() {
      this.drawer = true;
      this.caseTitle = "创建用例";
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val;
      this.initCaseList(this.currentModule, this.req);
    },
  },
};
</script>

<style scoped>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
