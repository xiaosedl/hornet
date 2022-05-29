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
    </div>
    <div class="block">
      <el-card style="width: 30%; margin-top: 20px">
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
        >
          <span class="custom-tree-node" slot-scope="{ node, data }">
            <span>{{ node.label }}</span>
            <span>
              <el-button type="text" size="mini" @click="() => append(data)">
                <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)"
              >
                <i class="el-icon-remove-outline"></i>
              </el-button>
            </span>
          </span>
        </el-tree>
      </el-card>
    </div>
    <!--组件中，引入子组件-->
    <moduleDialog
      v-if="dialogFlag"
      :pid="projectValue"
      :plabel="projectLabel"
      :rootId="rootFlag"
      @cancel="closeDialog"
    ></moduleDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import ModuleApi from "../../request/module";
import moduleDialog from "./moduleDialog";

let id = 1000;

export default {
  name: "caseModule",
  components: {
    moduleDialog,
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
    async initModuleList(pid) {
      const req = { project_id: pid };
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
      console.log("data:", data);
      const newChild = { id: id++, label: "testtest", children: [] };
      if (!data.children) {
        this.$set(data, "children", []);
      }
      data.children.push(newChild);
    },

    // 删除节点
    remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      children.splice(index, 1);
    },

    // 展示创建弹窗
    createRootDialog() {
      this.dialogFlag = true;
      this.rootFlag = 1;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.initModuleList(this.projectValue);
    },

    // 跟节点弹窗
  },
};
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
