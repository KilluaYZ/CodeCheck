<template>
    <el-row style="width: 100%; height: 100%">
        <el-row style="width: 50%; height: 100%;padding: 15px 20px 15px 20px; background: #2c3e50">
            <el-row style="width: 100%; height: 100%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%; height: 100%;">

                </el-row>
            </el-row>
        </el-row>
        <el-row style="width: 50%; height: 100%; padding: 15px 20px 15px 20px; background: #74ebd5; flex-direction: column; justify-content: space-between; align-items: center">
            <el-row style="width: 100%; height: 20%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%; height: 100%; justify-content: space-evenly; align-items: center;">
                    <el-row style="">
                        <el-button type="success" size="large"><el-icon><VideoPlay /></el-icon>开始Fuzz</el-button>
                        <el-button type="danger" size="large"><el-icon><VideoPause /></el-icon>停止Fuzz</el-button>
                        <el-button type="primary" size="large"><el-icon><Refresh /></el-icon>刷新Queue</el-button>
                    </el-row>
                </el-row>
            </el-row>
            <el-row style="width: 100%; height: 78%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%; height: 100%; ">

                </el-row>
            </el-row>
        </el-row>
    </el-row>
</template>

<script setup lang="ts">

import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ProjectType } from '@/types'
import { getProjectDetail } from '@/api/project'
import { Refresh, VideoPause, VideoPlay } from '@element-plus/icons-vue'

const router = useRouter();
const route  = useRoute();
const projectId = route.query.projectId as string
const project_info = ref<ProjectType>();
const get_project_info = () => {
    getProjectDetail(projectId)
        .then(res => {
            project_info.value = res.data;
        })
}

onMounted(get_project_info)

</script>

<style>
.card-eff{
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)
}
</style>