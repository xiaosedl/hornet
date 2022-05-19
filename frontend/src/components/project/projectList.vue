<template>
  <div class="project">
    <h1>这是一个 Project 页面</h1>
    <el-card class="box-card">
      <div style="text-align: right">
        <el-button type="primary" style="height: 50px">创建</el-button>
      </div>
      <div v-for="o in tableData" :key="o.id" class="text item">
        <el-col :span="7" class="project-card">
          <el-card style="width: 95%; height: 400px">
            <div slot="header" class="clearfix">
              <span>{{ o.name }}</span>
              <el-button style="float: right; padding: 3px 0" type="text"
                >操作按钮</el-button
              >
            </div>
          {{ o.describe }}
          </el-card>
        </el-col>
      </div>
    </el-card>
  </div>
</template>

<script>
import ProjectApi from "../../request/project"

export default {
  data() {
    return {
      tableData: [],
      req: {
        page: 1,
        size: 5
      }
    };
  },
  created() {
    this.initProject()
  },
  methods: {
    async initProject() {
      const resp = await ProjectApi.getProjects(this.req);
      console.log("--->", resp);
      if (resp.success === true) {
        this.tableData = resp.items;
        this.$message.success("查询成功！");
      } else {
        this.$message.error("查询失败")
      }
    }
  },
};
</script>
