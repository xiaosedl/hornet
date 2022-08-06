<template>
  <div style="margin: 20px">
    <div class="div-line" style="float: left; width: 100%">
      <div style="float: left; width: 15%">
        <el-select
          v-model="caseForm.method"
          size="small"
          clearable
          placeholder="请选择"
        >
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
          v-model="caseForm.url"
          size="small"
          clearable
          placeholder="请输入 URL"
        ></el-input>
      </div>
      <div style="float: right">
        <el-button type="primary" size="small" @click="clickSend"
          >发送</el-button
        >
      </div>
    </div>
    <div class="div-line" style="float: left; margin: 20px 0">
      <el-radio v-model="caseForm.params_type" label="Params">Params</el-radio>
      <el-radio v-model="caseForm.params_type" label="Form">Form-data</el-radio>
      <el-radio v-model="caseForm.params_type" label="Json">JSON</el-radio>
    </div>
    <div class="div-line" style="float: left; width: 100%">
      <el-tabs v-model="activeName">
        <el-tab-pane label="Header" name="first">
          <vueJsonEditor
            v-model="caseForm.header"
            :mode="'code'"
          ></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor
            v-model="caseForm.params_body"
            :mode="'code'"
          ></vueJsonEditor
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
          <div class="div-line" style="float: left; margin: 10px 0">
            <el-radio
              v-model="caseForm.assert_type"
              name="include"
              label="include"
              >Include</el-radio
            >
            <el-radio v-model="caseForm.assert_type" label="equal"
              >Equal</el-radio
            >
            <el-button
              style="float: right"
              type="success"
              size="small"
              @click="clickAssert"
              >断言</el-button
            >
          </div>
          <div class="div-line">
            <el-input
              type="textarea"
              :rows="6"
              placeholder="Assert Content"
              v-model="caseForm.assert_text"
            >
            </el-input>
          </div>
        </el-collapse-item>
        <el-collapse-item title="提取器" name="2">
          <el-form>
            <div v-for="(item, index) in extractList" :key="index">
              <el-form-item label="提取">
                <el-col :span="7">
                  <el-input
                    v-model="item.name"
                    placeholder="变量"
                    style="width: 100%"
                  ></el-input>
                </el-col>
                <el-col :span="12">
                  <el-input
                    v-model="item.extract"
                    placeholder="提取规则"
                    style="width: 100%"
                  ></el-input>
                </el-col>
              </el-form-item>
            </div>
          </el-form>
          <div class="div-line" style="float: left; margin: 10px 0">
            <el-button
              style="float: left"
              type="success"
              size="small"
              @click="addExtract"
              icon="el-icon-plus"
              >添加</el-button
            >
            <el-button
              style="float: left"
              type="primary"
              size="small"
              @click="checkExtract"
              >检查</el-button
            >
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
        <el-button type="primary" size="small" @click="clickSave"
          >保存</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import vueJsonEditor from "vue-json-editor";
import CaseApi from "../../request/case";

export default {
  name: "caseDialog",
  props: ["mid", "cid", "drawerFlag", "caseTitle"],
  components: {
    vueJsonEditor,
  },
  data() {
    return {
      methodOptions: [
        {
          value: "GET",
          label: "GET",
        },
        {
          value: "POST",
          label: "POST",
        },
        {
          value: "PUT",
          label: "PUT",
        },
        {
          value: "DELETE",
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
        url: "http://httpbin.org/post",
        name: "",
        method: "POST",
        header: { token: "123" },
        params_type: "Json",
        params_body: {},
        response: "",
        assert_type: "include",
        assert_text: "",
        extract_list: [],
      },
      extractList: [],
    };
  },

  mounted() {
    this.caseForm.module_id = this.mid;
    if (this.cid !== 0) {
      this.getCaseDetail();
    }
  },

  methods: {
    // 获取用例详情
    async getCaseDetail() {
      const resp = await CaseApi.detailCase(this.cid);
      if (resp.success === true) {
        this.$message.success("用例详情获取成功");
        this.caseForm = resp.item;
        this.caseForm.module_id = resp.item.module;
        this.extractList = resp.item.extract_list;
        const header = resp.item.header.replace(/'/g, '"');
        const params_body = resp.item.params_body.replace(/'/g, '"');
        this.caseForm.header = JSON.parse(header);
        this.caseForm.params_body = JSON.parse(params_body);
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 发送
    async clickSend() {
      const resp = await CaseApi.debugCase(this.caseForm);
      if (resp.success === true) {
        this.$message.success("请求成功");
        this.caseForm.response = resp.item.response;
      } else {
        this.$message.error(resp.error.msg);
      }
    },

    // 点击断言
    async clickAssert() {
      const req = {
        response: this.caseForm.response,
        assert_type: this.caseForm.assert_type,
        assert_text: this.caseForm.assert_text,
      };
      const resp = await CaseApi.assertCase(req);
      if (resp.success === true) {
        this.$message.success("断言成功");
      } else {
        this.$message.error("断言失败");
      }
    },

    // 保存用例
    async clickSave() {
      this.caseForm.extract_list = this.extractList;
      if (this.cid === 0) {
        const resp = await CaseApi.createCase(this.caseForm);
        if (resp.success === true) {
          this.$message.success("保存用例成功");
          this.drawerFlag = false;
        } else {
          this.$message.error(resp.error.msg);
        }
      } else {
        const resp = await CaseApi.updateCase(this.cid, this.caseForm);
        if (resp.success === true) {
          this.$message.success("保存用例成功");
          this.drawerFlag = false;
        } else {
          this.$message.error(resp.error.msg);
        }
      }
    },

    // 增加提取器
    addExtract() {
      this.extractList.push({ name: "", extract: "" });
    },

    // 检查提取器
    async checkExtract() {
      if (this.extractList.length === 0) {
        this.$message.error("请添加提取器");
        return;
      }
      const req = {
        response: this.caseForm.response,
        extract_list: this.extractList,
        module_id: this.mid,
        case_id: this.cid,
      };
      const resp = await CaseApi.checkExtract(req);
      if (resp.success === true) {
        this.$message.success("检查成功");
      } else {
        this.$message.error(resp.error.msg);
      }
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
  margin-top: 0;
  padding-top: 0;
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
