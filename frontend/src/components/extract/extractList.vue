<template>
  <div class="repost">
    <div style="text-align: left">
      <el-form :inline="true" :model="projectForm" class="demo-form-inline">
        <el-form-item label="项目">
          <el-select
            v-model="projectForm.id"
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
      </el-form>
    </div>
    <div>
      <el-table
        :data="extractData"
        border
        header-align="center"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" style="width: 5%" align="center">
        </el-table-column>
        <el-table-column
          prop="name"
          label="变量名称"
          style="width: 25%"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="value"
          label="变量值"
          style="width: 10%"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="extract"
          label="提取规则"
          style="width: 10%"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="create_time"
          label="创建时间"
          style="width: 25%"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="update_time"
          label="更新时间"
          style="width: 25%"
          align="center"
        ></el-table-column>

        <el-table-column
          prop="status"
          label="操作"
          style="width: 10%"
          align="center"
        >
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="showExtract(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteExtract(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
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
    <extractDialog
      v-if="dialogFlag"
      :rid="extractId"
      @cancel="closeDialog"
    ></extractDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import extractDialog from "../../components/extract/extractDialog";
import ExtractApi from "../../request/extract";

export default {
  name: "Extract",
  components: {
    extractDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      projectOptions: [],
      dialogFlag: false,
      extractId: "",
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
      extractData: [],
    };
  },

  created() {
    // 加载 vue 组件同时获取项目列表
    this.initProjectList();
  },

  mounted() {
    this.initExtractList();
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
        this.$message.error(resp.error.msg);
      }
    },

    // 修改选中的项目
    changeProject(value) {
      this.projectForm.id = value;
      this.initExtractList();
    },

    // 初始化提取器管理列表
    async initExtractList() {
      const req = {
        project_id: this.projectForm.id,
        page: this.req.page,
        size: this.req.size,
      };
      const resp = await ExtractApi.getExtracts(req);
      if (resp.success === true) {
        this.extractData = resp.items;
        this.total = resp.total;
      } else {
        this.$message.error(resp.error.mag);
      }
    },

    // 展示提取器详情弹窗
    showExtract(row) {
      this.extractId = row.id;
      this.dialogFlag = true;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.initExtractList();
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val;
      this.initExtractList();
    },
  },
};
</script>
