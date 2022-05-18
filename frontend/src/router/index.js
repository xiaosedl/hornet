import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Navigation from "../views/Navigation";
import About from "../views/About";
import project from "../components/project/projectList";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
  {
    path: "/main",
    name: "Navigation",
    component: Navigation,
    children: [
      {
        // 当 /main/home 匹配成功，
        // Home 会被渲染在 Navigation 的 <router-view> 中
        path: "home",
        component: Home,
      },
      {
        path: "about",
        component: About,
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        // component: () =>
        //     import(/* webpackChunkName: "about" */ "../views/About.vue"),
      },
      {
        // 当 /main/home 匹配成功，
        // Home 会被渲染在 Navigation 的 <router-view> 中
        path: "project",
        component: project,
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// 导航守卫，控制一些页面登录才能访问
router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    // 当路由为 Login 时就直接下一步动作
    next();
  } else {
    // 否则就需要判断
    if (sessionStorage.token) {
      // 如果有用户名就进行下一步 sessionStorage 浏览器提供的缓存
      next();
    } else {
      next({ path: "/login" }); // 没有用户名就跳转到 login 页面
    }
  }
});

export default router;
