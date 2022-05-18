<template>
  <div class="navigation">
    <el-container class="el-container">
      <el-aside width="200px" style="background-color: #1e2531">
        <img class="logo" src="../assets/logo.svg" alt="logo" />
        <el-menu style="background-color: #1e2531">
          <router-link to="/main/project">
            <el-menu-item
              index="1"
              class="menu-option"
              style="color: dodgerblue"
            >
              <i class="el-icon-menu"></i>
              <template #title>项目管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/about">
            <el-menu-item
              index="1"
              class="menu-option"
              style="color: dodgerblue"
            >
              <template #title> <i class="el-icon-s-home"></i>About </template>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="el-header" style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>欢迎～{{ user }}</span>
        </el-header>
        <el-main class="el-main">
          <h1>这个位置渲染子组件</h1>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.navigation {
  height: 100%;
}

.el-container {
  height: 100%;
  border: 1px solid #eee;
}

.el-main {
  margin: 3px;
  background-color: whitesmoke;
}

a {
  text-decoration: none;
}

el-aside {
  color: #333;
}
</style>

<script>
export default {
  data() {
    return {
      user: "",
    };
  },
  created() {
    this.user = sessionStorage.getItem("user");
  },
};
</script>
