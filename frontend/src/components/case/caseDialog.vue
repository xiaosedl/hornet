<template>
  <div style="margin: 20px">
    <div class="div-line" style="float: left; width: 100%">
      <div style="float: left; width: 15%">
        <el-select v-model="value" size="small" clearable placeholder="请选择">
          <el-option
            v-for="method in methodOptions"
            :key="method.value"
            :label="method.label"
            :value="method.value"
          >
          </el-option>
        </el-select>
      </div>
      <div style="float: left; margin: 0 1px; width: 76%">
        <el-input
          v-model="input"
          size="small"
          clearable
          placeholder="请输入 URL"
        ></el-input>
      </div>
      <div style="float: right">
        <el-button type="primary" size="small">发送</el-button>
      </div>
    </div>
    <div class="div-line" style="float: left; margin: 20px 0">
      <el-radio v-model="paramType" label="1">Params</el-radio>
      <el-radio v-model="paramType" label="2">Form-data</el-radio>
      <el-radio v-model="paramType" label="3">JSON</el-radio>
    </div>
    <div class="div-line" style="float: left; width: 100%">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="Header" name="first">
          <vueJsonEditor v-model="json" :mode="'code'"></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor v-model="json" :mode="'code'"></vueJsonEditor
        ></el-tab-pane>
      </el-tabs>
    </div>
    <div class="div-line">
      <el-input
        type="textarea"
        :rows="6"
        placeholder="Response"
        v-model="caseForm.response"
      >
      </el-input>
    </div>
    <div class="div-line">
      <el-collapse v-model="activeNames" accordion>
        <el-collapse-item title="断言" name="1">
          <div class="div-line" style="float: left; margin: 20px 0">
            <el-radio
              v-model="caseForm.assert_type"
              name="include"
              label="include"
              >Include</el-radio
            >
            <el-radio v-model="caseForm.assert_type" label="equal"
              >Equal</el-radio
            >
            <el-button style="float: right" type="success" size="small"
              >断言</el-button
            >
          </div>
          <div class="div-line">
            <el-input
              type="textarea"
              :rows="6"
              placeholder="Assert Content"
              v-model="caseForm.assert_type"
            >
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="div-line" style="float: left; width: 100%; margin: 10px 0">
      <div style="float: left; margin: 0 1px; width: 91%">
        <el-input
          v-model="caseForm.name"
          size="small"
          clearable
          placeholder="请输入用例名称"
        ></el-input>
      </div>
      <div style="float: right; margin-bottom: 50px">
        <el-button type="primary" size="small">保存</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import vueJsonEditor from "vue-json-editor";

export default {
  name: "caseDialog",
  components: {
    vueJsonEditor,
  },
  data() {
    return {
      methodOptions: [
        {
          value: "get",
          label: "GET",
        },
        {
          value: "post",
          label: "POST",
        },
        {
          value: "put",
          label: "PUT",
        },
        {
          value: "delete",
          label: "DELETE",
        },
      ],
      value: "",
      input: "",
      paramType: "1",
      activeName: "first",
      json: {
        id: 123,
        name: "json",
      },
      textarea: "",
      assertType: "include",
      activeNames: "include",
      caseForm: {
        module_id: 0,
        url: "",
        name: "",
        method: "",
        header: "",
        params_type: "params",
        params_body: {},
        response: "",
        assert_type: "include",
        assert_text: "",
      },
    };
  },
  methods: {
    // tab 页控制
    handleClick(tab, event) {
      console.log(tab, event);
    },

    // json 输入框默认方法
    onJsonChange(value) {
      console.log("value:", value);
    },
  },
};
</script>

<style>
div.jsoneditor {
  border: thin solid #ced4da;
}
div.jsoneditor-menu {
  display: none;
}
.ace-jsoneditor .ace_gutter {
  background: white;
}
div.jsoneditor-outer.has-main-menu-bar {
  margin-top: 0px;
  padding-top: 0px;
}
.per-label {
  margin-right: 10px;
  margin-bottom: 4px;
  font-size: 1rem;
}
</style>

<style scoped>
.debug-button {
  float: right;
  margin-right: 20px;
}
.div-line {
  height: auto;
  width: 100%;
  text-align: left;
  margin-bottom: 10px;
}
</style>
