<template>
  <div class="case">
    <div style="float: left; line-height: 40px; margin-right: 20px">
      <strong>项目</strong>
    </div>
    <div style="text-align: left">
      <el-select
        v-model="projectValue"
        placeholder="请选择"
        @change="changeProject"
      >
        <el-option
          v-for="item in projectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        >
        </el-option>
      </el-select>
      <el-button
        @click="caseCreate"
        type="primary"
        style="margin-left: 16px; float: right"
      >
        点我打开
      </el-button>
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
          default-expand-all
          :expand-on-click-node="false"
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
        style="width: 70%; margin: 20px 0; float: right;"
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
          width="180"
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
    </div>

    <el-drawer
      :title="caseTitle"
      v-model="drawer"
      :visible.sync="drawer"
      direction="rtl"
      size="50%"
    >
      <!--引入用例抽屉子组件-->
      <caseDialog></caseDialog>
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
    };
  },

  mounted() {
    // 加载 vue 组件同时初始化模块列表
    this.initProjectList();
    this.initModuleList(this.projectValue);
  },

  methods: {
    // 初始化项目列表
    async initProjectList() {
      const resp = await ProjectApi.getProjects(this.req);
      console.log("initProjectList--->", resp);
      if (resp.success === true) {
        this.moduleData = resp.items;
        this.projectValue = resp.items[0].id;
        this.projectLabel = resp.items[0].name;
        // 处理图片访问路径
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
      console.log("changeProject: ", value);
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
      console.log("getModules--->", resp.items);
      if (resp.success === true) {
        this.moduleData = resp.items;
      } else {
        this.$message.error("查询失败");
      }
    },

    // 创建子节点
    append(data) {
      console.log("新增子模块", data);
      this.dialogFlag = true;
      this.rootFlag = false;
      this.parentObj = data;
    },

    // 删除节点
    remove(data) {
      console.log("删除子模块", data);
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

    // 点击了节点
    nodeClick(data) {
      console.log("点击了节点", data);
      this.initCaseList(data.id);
    },

    // 初始化用例
    async initCaseList(mid) {
      const resp = await ModuleApi.getModuleCases(mid);
      if (resp.success === true) {
        console.log("case", resp);
        this.caseData = resp.items;
        this.$message.success("查询用例成功");
      } else {
        this.$message.error(resp.error.mag);
      }
    },

    // 点击用例，弹出抽屉，查看用例
    caseRowClick(row) {
      console.log("row", row);
      this.drawer = true;
      this.caseTitle = "查看用例";
    },

    // 创建用例
    caseCreate() {
      this.drawer = true;
      this.caseTitle = "创建用例";
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
