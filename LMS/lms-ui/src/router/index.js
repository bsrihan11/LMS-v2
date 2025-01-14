import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Main/Home.vue'
import MainView from "@/views/Main/Main.vue"

import store from '@/store'
const routes = [
  {
    path: '/',
    name: 'Main',
    component: MainView,
    redirect: "/home",
    children: [{
      path: "/home",
      name: "home_view",
      components: {
        main: HomeView
      },
    },
    {
      path: "/profile",
      name: 'profile_view',
      components: {
        main: () => import(/* webpackChunkName: "profile_view" */ '../views/Main/Profile.vue')
      }
    },
    {
      path: "/book/:book_id(\\d+)",
      name: 'book_view',
      components: {
        main: () => import(/* webpackChunkName: "book_view" */ '../views/Main/BookDesc.vue')
      }
    },
    {
      path: '/section/:section_id(\\d+)',
      name: 'section_view',
      components: {
        main: () => import(/* webpackChunkName: "section_view" */ '../views/Main/Section.vue')
      }
    },
    {
      path: "/search",
      name: 'search_view',
      components: {
        main: () => import(/* webpackChunkName: "search_view" */ '../views/Main/Search.vue')
      }
    },
    {
      path: '/error',
      name: 'internal_error',
      components: {
        main: () => import(/* webpackChunkName: "internal_error" */ '../views/Error.vue')
      }
    }
    ]
  },
  {
    path: '/auth/:formType',
    name: "auth_view",
    beforeEnter: async (to, from, next) => {
      const allowedValues = ['update-user', 'login', 'register'];
      if (allowedValues.includes(to.params.formType)) {
        if (to.params.formType === 'update-user') {

          await store.dispatch('auth/loadUser')
          next();
        }
        else {
          next()
        }
      } else {
        next('/error');
      }
    },
    components: {
      default: () => import(/* webpackChunkName: "auth_view" */ '../views/Auth.vue')
    }
  },
  {
    path:'/pdf/:book_id',
    name:'pdf_view',
    component: () => import(/* webpackChunkName: "pdf_view" */ '../components/PDF.vue')
  },
  {
    path: '/master',
    name: 'master',
    component: () => import(/* webpackChunkName: "master" */ '../views/Master/Master.vue'),
    children: [
      {
        path: 'login',
        name: 'master_login',
        components: { master: () => import(/* webpackChunkName: "master_login" */ '../views/Master/MasterLogin.vue') }

      },
      {
        path: 'admin',
        name: 'admin_view',
        components: { master: () => import(/* webpackChunkName: "admin_view" */ '../views/Master/Admin/Admin.vue') }
        ,
        children: [
          {
            path: 'dashboard',
            name: 'admin_dashboard',
            components: {
              admin: () => import(/* webpackChunkName: "admin_dashboard" */ '../views/Master/Admin/Dashboard.vue')
            }
          },
          {
            path: 'update',
            name: 'admin_user_update',
            components: {
              admin: () => import(/* webpackChunkName: "admin_user_update" */ '../views/Master/Admin/AdUpdateUser.vue')
            }

          }
        ]

      },
      {
        path: 'manager',
        name: 'manager_view',
        components: { master: () => import(/* webpackChunkName: "manager_view" */ '../views/Master/Manager/Manager.vue') },
        children: [
          {
            path: 'book',
            name: 'book_crud',
            components: {
              manager: () => import(/* webpackChunkName: "book_crud" */ '../views/Master/Manager/BookCRUD.vue')
            }
          },
          {
            path: 'section',
            name: 'section_crud',
            components: {
              manager: () => import(/* webpackChunkName: "section_crud" */ '../views/Master/Manager/SectionCRUD.vue')
            }
          },
          {
            path: 'author',
            name: 'author_crud',
            components: {
              manager: () => import(/* webpackChunkName: "author_crud" */ '../views/Master/Manager/AuthorCRUD.vue')
            }
          }

        ]
      }
    ]
  },

  {
    path: '/:pathMatch(.*)*',
    redirect: to => {
      return { path: '/error' }
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})




export default router