<template>
  <el-dialog
    :title="showTitle"
    :visible.sync="dialogVisible"
    width="900px"
    :before-close="closeDialog"
  >
    <div
      id="echart"
      :style="{ width: '380px', height: '380px' }"
      style="margin: 0 auto"
    ></div>
    <div style="margin: 20px 0">
      <el-table
        :data="reportData"
        border
        header-align="center"
        style="width: 100%"
      >
        <el-table-column
          prop="tests"
          label="总数"
          style="width: 5%"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="success">{{ scope.row.tests }}</el-tag>
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
      </el-table>
    </div>
    <el-form
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="详情日志：">
        <el-input type="textarea" :rows="10" v-model="detailLog"></el-input>
      </el-form-item>
      <div>
        <el-form-item style="text-align: right">
          <div class="dialog-footer">
            <el-button @click="closeDialog">取消</el-button>
          </div>
        </el-form-item>
      </div>
    </el-form>
  </el-dialog>
</template>

<script>
import * as echarts from "echarts";
import ReportApi from "../../request/report";

export default {
  name: "extractDialog",
  props: ["rid"],
  data() {
    return {
      showTitle: "报告详情",
      dialogVisible: true,
      rules: {
        name: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
      },
      reportData: [],
      detailLog: "",
      chartOption: {
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "占比",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "40",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [],
          },
        ],
      },
    };
  },

  mounted() {
    // Error: Initialize failed: invalid dom.原因：图表在弹窗渲染之前就渲染了
    // 导致弹窗获取不到图表元素，正常应先等待弹窗渲染完后再渲染图表
    this.$nextTick(() => {
      this.initEChart();
    });
  },

  methods: {
    // 初始化图表
    async initEChart() {
      let chartDom = document.getElementById("echart");
      const resp = await ReportApi.getReportDetail(this.rid);
      if (resp.success === true) {
        this.reportData.push(resp.item);
        this.chartOption.series[0].data.push({
          value: resp.item.passed,
          name: "通过",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.failure,
          name: "失败",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.skipped,
          name: "跳过",
        });
        this.chartOption.series[0].data.push({
          value: resp.item.error,
          name: "错误",
        });
        this.detailLog = resp.item.result;
        this.showTitle = resp.item.name + " 报告详情";
      }
      let myChart = echarts.init(chartDom);
      myChart.setOption(this.chartOption);
    },

    // 关闭弹窗
    closeDialog() {
      // 关闭弹窗，子组件回调给父组件，在父组件中引入子组件的地方绑定 cancel 事件 @cancel="xxx"
      this.$emit("cancel", {});
    },
  },
};
</script>
