<template>
  <el-container style="height: 900px; border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <el-menu>
        <router-link to="/main/home">
          <el-menu-item index="1" class="menu-option">
            <template #title>
              <i class="el-icon-s-home"></i>Home
            </template>
          </el-menu-item>
        </router-link>
        <router-link to="/main/about">
          <el-menu-item index="1" class="menu-option">
            <template #title>
              <i class="el-icon-s-home"></i>About
            </template>
          </el-menu-item>
        </router-link>

      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
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

      <el-main>
        <h1>这个位置渲染子组件</h1>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>

<script>
export default {
  data() {
    return {
      user: "",
    }
  },
  created() {
     this.user = sessionStorage.getItem('user')
  }
};
</script>