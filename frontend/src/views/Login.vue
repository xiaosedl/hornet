<template>
  <div class="home">
    <div class="main-window">
      <div class="main-desc">
        <h2>接口测试平台</h2>
        <p>项目管理、模块用例管理、任务执行、测试报告等功能</p>
      </div>
      <div class="login-window">
        <el-card class="box-card">
          <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="登录" name="first">
              <el-form
                :model="loginForm"
                :rules="rules"
                ref="loginForm"
                label-position="left"
                label-width="100px"
                class="demo-ruleForm"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input
                    v-model="loginForm.username"
                    cy-data="LoginUsername"
                  ></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <el-input
                    v-model="loginForm.password"
                    type="password"
                    cy-data="LoginPassword"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button
                    style="width: 258px"
                    type="primary"
                    @click="submitLogin('loginForm')"
                    cy-data="LoginSubmit"
                    >登录</el-button
                  >
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="注册" name="second">
              <el-form
                :model="registerForm"
                :rules="rules"
                ref="registerForm"
                label-position="left"
                label-width="100px"
                class="demo-ruleForm"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="registerForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <el-input
                    v-model="registerForm.password"
                    type="password"
                  ></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="password">
                  <el-input
                    v-model="registerForm.confirm_password"
                    type="password"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button
                    style="width: 258px"
                    type="primary"
                    @click="submitRegister('registerForm')"
                    >注册</el-button
                  >
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src-->
// import HelloWorld from "@/components/HelloWorld.vue";

import UserAPi from "../request/user";

export default {
  data() {
    return {
      activeName: "first",
      loginForm: {
        username: "",
        password: "",
      },
      registerForm: {
        username: "",
        password: "",
        confirm_password: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        confirm_password: [
          { required: true, message: "请输入确认密码", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    // 用户登录
    submitLogin(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert("submit!");
          UserAPi.login(this.loginForm).then((resp) => {
            console.log("login", resp);
            if (resp.success === true) {
              sessionStorage.token = resp.item.token;
              sessionStorage.user = resp.item.username;
              this.$router.push({ path: "/main" });
              this.$message.success("登录成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 用户注册
    submitRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert("submit!");
          UserAPi.register(this.registerForm).then((resp) => {
            console.log("login", resp);
            if (resp.success === true) {
              // sessionStorage.token = resp.item.token
              // sessionStorage.user = resp.item.username
              // this.$router.push({ path: "/home"})
              this.$message.success("注册成功！");
            } else {
              this.$message.error(resp.error.msg);
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>

<style>
.main-window {
  margin: 0 auto;
  width: 900px;
  padding-top: 18%;
}

.main-desc {
  float: left;
  width: 350px;
}

.login-window {
  float: left;
  width: 400px;
  margin-left: 50px;
}
</style>
