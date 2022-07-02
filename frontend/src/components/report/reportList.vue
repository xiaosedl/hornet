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
        :data="reportData"
        border
        header-align="center"
        style="width: 100%;"
      >
        <el-table-column prop="id" label="ID" style="width: 5%" align="center">
        </el-table-column>
        <el-table-column
          prop="name"
          label="报告名称"
          style="width: 25%"
          header-align="center"
        >
        </el-table-column>
        <el-table-column
          prop="tests"
          label="总数"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag>{{ scope.row.tests }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="passed"
          label="通过"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="success">{{ scope.row.passed }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="error"
          label="错误"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="danger">{{ scope.row.error }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="failure"
          label="失败"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="warning">{{ scope.row.failure }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="skipped"
          label="跳过"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="info">{{ scope.row.skipped }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="runtime"
          label="运行时长"
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
          prop="status"
          label="操作"
          style="width: 10%"
          align="center"
        >
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="showReport(scope.row)"
              >查看</el-button
            >
            <el-button type="text" size="small" @click="deleteReport(scope.row)"
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
    <reportDialog
      v-if="dialogFlag"
      :rid="reportId"
      @cancel="closeDialog"
    ></reportDialog>
  </div>
</template>

<script>
import ProjectApi from "../../request/project";
import reportDialog from "../../components/report/reportDialog";
import ReportApi from "../../request/report";

export default {
  name: "Report",
  components: {
    reportDialog,
  },
  data() {
    return {
      projectForm: {
        id: 1,
      },
      projectOptions: [],
      dialogFlag: false,
      reportId: "",
      req: {
        page: 1,
        size: 6,
      },
      total: 50,
      reportData: [],
    };
  },

  created() {
    // 加载 vue 组件同时获取项目列表
    this.initProjectList();
  },

  mounted() {
    this.initReportList();
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
      this.initTaskList();
    },

    // 初始化测试报告列表
    async initReportList() {
      const req = {
        project_id: this.projectForm.id,
        page: this.req.page,
        size: this.req.size,
      };
      const resp = await ReportApi.getReports(req);
      if (resp.success === true) {
        this.reportData = resp.items;
        this.total = resp.total;
      } else {
        this.$message.error(resp.error.mag);
      }
    },

    // 展示报告详情弹窗
    showReport(row) {
      this.reportId = row.id;
      this.dialogFlag = true;
    },

    // 关闭弹窗
    closeDialog() {
      this.dialogFlag = false;
      this.initReportList();
    },

    // 分页方法，跳转到第几页
    handleCurrentChange(val) {
      this.req.page = val;
      this.initReportList();
    },
  },
};
</script>
