<template>
    <div class="nav">
        <div class="nav-left">
            <el-icon class="pointer mr20" size="20" @click="useStore.changeCollapse">
                <Fold v-if="!useStore.isCollapse" />
                <Expand v-if="useStore.isCollapse" />
            </el-icon>

            <Crumb></Crumb>
        </div>
        <div class="nav-right">
            <el-icon @click="OpenFullScreen" size="16" class="pointer"><FullScreen /></el-icon>
            <div class="user ml20 flex pointer">
                <el-avatar
                    src="http://thirdqq.qlogo.cn/g?b=oidb&k=REYMpW1m0CGfb5pHYeaibvQ&s=100&t=1624209837"
                ></el-avatar>
                <el-dropdown class="ml20">
                    <span class="el-dropdown-link">
                        {{userInfo.username}}
                        <el-icon class="el-icon--right">
                            <arrow-down />
                        </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item>个人中心</el-dropdown-item>
                            <el-dropdown-item @click="isVisible = !isVisible">退出登陆</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
    </div>

    <custom-dialog v-model="isVisible" dialogTitle="是否退出登陆" dialogWidth="500">
        <p style="font-size: 16px; color: #333;padding-left: 20px;">你确定要退出登陆吗？</p>
        <template #footer>
            <el-button @click="logout" type="primary">确定</el-button>
            <el-button @click="isVisible = !isVisible" type="info">取消</el-button>
        </template>
    </custom-dialog>
</template>

<script setup lang="ts">
import { useMenuStore } from '@/store/menu'
import { onMounted, ref } from 'vue'
import Crumb from './Crumb.vue'
import { Storage } from '@/utils/cache'
import { getUserInfo } from '@/utils/auth'

const useStore = useMenuStore()
const isVisible = ref(false)
const userInfo = ref({});
/**
 * 进入全屏
 */
const OpenFullScreen = () => {
    let element = document.documentElement
    document.fullscreenElement ? document.exitFullscreen() : element.requestFullscreen()
    // console.log('d', document.fullscreenElement)
}

const logout = () => {

    Storage.removeItem('userInfo')
    Storage.removeItem('token')
    location.reload()
}

const initInfo = () => {
    userInfo.value =  getUserInfo()
    console.log(userInfo.value)
}

onMounted(initInfo)
</script>

<style scoped lang="scss">
$height: 70px;
.nav {
    @include flex(center, space-between);
    height: $height;
    .nav-left {
        @include flex(center);
    }
    .nav-right {
        @include flex(center);
    }
    .flex {
        @include flex(center);
    }
}
</style>
