<template>
  <div class="project">
    <h1>这是一个 Project 页面</h1>
    <el-card class="box-card">
      <div style="text-align: right">
        <el-button type="primary" style="height: 50px">创建</el-button>
      </div>
      <div>
        <div v-for="o in tableData" :key="o" class="text item">
          <el-col :span="7" class="project-card">
            <el-card style="width: 95%; height: 400px">
              <div slot="header" class="clearfix">
                <span>{{ o.name }}</span>
                <el-button style="float: right; padding: 3px 0" type="text"
                  >操作按钮</el-button
                >
              </div>
              {{ o.address }}
            </el-card>
          </el-col>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1517 弄",
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
        },
      ],
    };
  },
};
</script>
