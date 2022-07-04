<template>
  <div class="navigation">
    <el-container
      class="el-container"
      style="height: 100%; border: 1px solid #eeeeee"
    >
      <el-aside width="200px" style="background-color: #1a2847">
        <div style="margin: 20px 0">
          <img class="logo" src="../assets/logo.svg" alt="logo" />
        </div>
        <el-menu
          default-active="onRoutes"
          background-color="#1a2847"
          text-color="#f1f2f6"
          active-text-color="#ffd04b"
        >
          <router-link to="/main/project">
            <el-menu-item index="1" class="menu-option">
              <i class="el-icon-menu"></i>
              <template #title>项目管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/case">
            <el-menu-item index="2" class="menu-option">
              <i class="el-icon-s-grid"></i>
              <template #title>用例管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/task">
            <el-menu-item index="3" class="menu-option">
              <i class="el-icon-s-order"></i>
              <template #title>任务管理</template>
            </el-menu-item>
          </router-link>
          <router-link to="/main/report">
            <el-menu-item index="4" class="menu-option">
              <i class="el-icon-s-data"></i>
              <template #title>报告管理</template>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>
      <el-container class="el-container-sub">
        <el-header class="el-header" style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span cy-data="LoginSuccess">欢迎～{{ user }}</span>
        </el-header>
        <el-main class="el-main">
          <el-card>
            <router-view></router-view>
          </el-card>
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
  margin: 1px;
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
  computed: {
    onRoutes() {
      if (this.$route.path === "/main/project") {
        return "1";
      } else if (this.$route.path === "/main/case") {
        return "2";
      } else if (this.$route.path === "/main/task") {
        return "3";
      } else if (this.$route.path === "/main/report") {
        return "4";
      }
      return "1";
    },
  },

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
