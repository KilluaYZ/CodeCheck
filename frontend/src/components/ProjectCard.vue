<template>
    <el-card shadow='hover' style='width: fit-content; min-width: 30%; max-width: 60%; margin: 10px'>
        <template #header>
           <el-row justify='space-between' align='middle' style='width: 100%;  align-items: center'>
               <el-col span=20>
                   <el-row align='middle'>
                       <span style='font-size: 24px;margin-right: 10px'>{{name}}</span>
                       <el-tag v-if='stage==="created"' type='warning'>已创建</el-tag>
                       <el-tag v-else-if='stage==="success"' type='success'>成功</el-tag>
                       <el-tag v-else-if='stage==="unzipping"'>正在解压源码</el-tag>
                       <el-tag v-else-if='stage==="analysing"' >正在分析源码</el-tag>
                       <el-tag v-else-if='stage==="pulling"' >正在拉取源码</el-tag>
                       <el-tag v-else-if='stage==="error"' type='danger' >失败</el-tag>
                       <el-tag v-else-if='stage==="waiting"' type='info' >正在排队等待</el-tag>
                       <el-tag v-else type='info'>状态未知</el-tag>
                   </el-row>
               </el-col>
               <el-col span=20>
                   <el-button type='primary' round @click='onClickEnterProjectBtn'>进入</el-button>
               </el-col>
           </el-row>
        </template>
        <el-row style='width: 100%'>
            <div v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</div>
        </el-row>
        <el-divider />
        <el-row style='width: 100%;' justify='space-between' align='middle'>
            <el-col span=20>
                <el-row>
                    <el-popover :visible="visible" placement="top" :width="160">
                        <p style='color: orangered;'>你确定要删除该项目吗？</p>
                        <div style="text-align: right; margin: 0">
                            <el-button size="small" text @click="visible = false">取消</el-button>
                            <el-button size="small" type="primary" @click="deleteFunc(id);visible = false">确定</el-button>
                        </div>
                        <template #reference>
<!--                            <el-button @click="visible = true" icon='DeleteFilled'></el-button>-->
                            <el-button @click='visible = true;' style='margin: 5px; margin-right: 10px;' circle :icon='Delete' type='danger'></el-button>
                        </template>
                    </el-popover>
                    <el-text>{{createTime}}</el-text>
                </el-row>
            </el-col>
            <el-col span=20>
                <el-tag v-if='isPublic' type='success'>公开</el-tag>
                <el-tag v-else type='info'>私有</el-tag>
            </el-col>
        </el-row>
    </el-card>
</template>

<script setup lang='ts'>
import { ref, defineProps } from 'vue';
import { delProject } from '@/api/project'
import { Delete } from '@element-plus/icons-vue'
import router from '@/router'
const visible = ref(false)
const props = defineProps({
    id: {
      required: true,
      type: Number
    },
    name: {
        required: true,
        type: String
    },
    stage:{
        required: false,
        type: String,
        default: 'unknown'
    },
    isPublic:{
        required: false,
        type: Boolean,
        default: false
    },
    createTime:{
        required: false,
        type: String,
        default: ''
    },
    deleteFunc:{
        required: true,
        type: Function
    }
})

const onClickDeleteBtn = () => {
    let projectId = props.id;
    props.deleteFunc(projectId);
}

const onClickEnterProjectBtn = () => {
    let routeUrl = router.resolve({
        path:"/project/detail",
        query: {projectId: props.id}
    });
    window.open(routeUrl.href, '_blank')
}

</script>

<style scoped>

</style>