/**
 * @author 爱呵呵
 * @description 组件路由模块
 */

import { RouteRecordRaw } from "vue-router";
import layout from '@/layout/index.vue'

const Project: Array<RouteRecordRaw> = [
    {
        path: '/project',
        component: layout,
        meta: { title: '项目', icon: 'MessageBox', activeMenu: true, orderNo: 1 },
        redirect: '/project/manage',
        children: [
            {
                path: 'manage',
                name: 'manage',
                meta: { title: '项目管理', keepAlive: false, icon: 'Tickets' },
                component: () => import('views/project/projectManage.vue')
            }
        ]
    },
]

export default Project;