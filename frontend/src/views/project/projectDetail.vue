<template>
    <el-row style="width: 100%; height: 100%">
        <el-row style="width: 50%; height: 100%;padding: 15px 20px 15px 20px; background: #2c3e50; flex-direction: column;justify-content: space-between; align-items: center">
            <el-row style="width: 100%; height: 80%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%; height: 100%;flex-direction: column; justify-content: center; align-items: center; flex-wrap: nowrap; padding: 10px 20px 10px 20px">
                    <el-row  style="width: 100%; background: #337ecc;">
                        <el-row style="width: 50%;">
                            <el-descriptions  title="process timing" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="run time">{{fuzz_stat.run_time}}</el-descriptions-item>
                                <el-descriptions-item  label="last new path">{{fuzz_stat.last_new_path}}</el-descriptions-item>
                                <el-descriptions-item  label="last uniq crash">{{fuzz_stat.last_uniq_crash}}</el-descriptions-item>
                                <el-descriptions-item  label="last uniq hang">{{fuzz_stat.last_uniq_hang}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                        <el-row style="width: 50%">
                            <el-descriptions  title="overall results" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="cycles done">{{fuzz_stat.cycles_done}}</el-descriptions-item>
                                <el-descriptions-item  label="total paths">{{fuzz_stat.total_path}}</el-descriptions-item>
                                <el-descriptions-item  label="uniq crashes">{{fuzz_stat.uniq_crashes}}</el-descriptions-item>
                                <el-descriptions-item  label="uniq hangs">{{fuzz_stat.uniq_hangs}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                    </el-row>
                    <el-row  style="width: 100%; background: #529b2e">
                        <el-row style="width: 50%">
                            <el-descriptions  title="cycle progress" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="now processing">{{fuzz_stat.now_processing}}</el-descriptions-item>
                                <el-descriptions-item  label="paths timed out">{{fuzz_stat.paths_timed_out}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                        <el-row style="width: 50%">
                            <el-descriptions  title="map coverage" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="map density">{{fuzz_stat.map_density}}</el-descriptions-item>
                                <el-descriptions-item  label="count coverage">{{fuzz_stat.count_coverage}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                    </el-row>
                    <el-row style="width: 100%; background: #c6e2ff">
                        <el-row style="width: 50%">
                            <el-descriptions  title="stage progress" :column="1"  style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="now trying">{{fuzz_stat.now_trying}}</el-descriptions-item>
                                <el-descriptions-item  label="stage execs">{{fuzz_stat.stage_execs}}</el-descriptions-item>
                                <el-descriptions-item  label="total execs">{{fuzz_stat.total_execs}}</el-descriptions-item>
                                <el-descriptions-item  label="exec speed">{{fuzz_stat.exec_speed}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                        <el-row style="width: 50%">
                            <el-descriptions  title="findings in depth" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="favored paths">{{fuzz_stat.favored_paths}}</el-descriptions-item>
                                <el-descriptions-item  label="new edges on">{{fuzz_stat.new_edges_on}}</el-descriptions-item>
                                <el-descriptions-item  label="total crashes">{{fuzz_stat.total_crashes}}</el-descriptions-item>
                                <el-descriptions-item  label="total tmouts">{{fuzz_stat.total_tmouts}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                    </el-row>
                    <el-row style="width: 100%; background: #d27373">
                        <el-row style="width: 50%;">
                            <el-descriptions  title="fuzzing strategy yields" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="bit flips">{{fuzz_stat.bit_flips}}</el-descriptions-item>
                                <el-descriptions-item  label="byte flips">{{fuzz_stat.byte_flips}}</el-descriptions-item>
                                <el-descriptions-item  label="arithmetics">{{fuzz_stat.arithmetics}}</el-descriptions-item>
                                <el-descriptions-item  label="known ints">{{fuzz_stat.known_inis}}</el-descriptions-item>
                                <el-descriptions-item  label="dictionary">{{fuzz_stat.dictionary}}</el-descriptions-item>
                                <el-descriptions-item  label="havoc">{{fuzz_stat.havoc}}</el-descriptions-item>
                                <el-descriptions-item  label="trim">{{fuzz_stat.trim}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                        <el-row style="width: 50%">
                            <el-descriptions  title="path geometry" :column="1" style="height: fit-content; width: 100%" size="small">
                                <el-descriptions-item  label="levels">{{fuzz_stat.levels}}</el-descriptions-item>
                                <el-descriptions-item  label="pending">{{fuzz_stat.pending}}</el-descriptions-item>
                                <el-descriptions-item  label="pend fav">{{fuzz_stat.pend_fav}}</el-descriptions-item>
                                <el-descriptions-item  label="own finds">{{fuzz_stat.own_finds}}</el-descriptions-item>
                                <el-descriptions-item  label="imported">{{fuzz_stat.imported}}</el-descriptions-item>
                                <el-descriptions-item  label="stability">{{fuzz_stat.stability}}</el-descriptions-item>
                                <el-descriptions-item  label="cpu">{{fuzz_stat.cpu}}</el-descriptions-item>
                            </el-descriptions>
                        </el-row>
                    </el-row>
                </el-row>
            </el-row>
            <el-row style="width: 100%; height: 18%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%; height: 100%;">
                    <el-row style="width: 100%; height: 100%; justify-content: space-evenly; align-items: center;">
                        <el-row style="">
                            <el-button type="success" size="large"><el-icon><VideoPlay /></el-icon>开始Fuzz</el-button>
                            <el-button type="danger" size="large"><el-icon><VideoPause /></el-icon>停止Fuzz</el-button>
                            <el-button type="warning" size="large"><el-icon><DArrowRight /></el-icon>跳过当前种子</el-button>
                            <el-button type="info" size="large"><el-icon><Setting /></el-icon>设置</el-button>
                        </el-row>
                    </el-row>
                </el-row>
            </el-row>
        </el-row>
        <el-row style="width: 50%; height: 100%; padding: 15px 20px 15px 20px; background: #74ebd5; flex-direction: column; justify-content: space-between; align-items: center">
            <el-row style="width: 100%; height: 28%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%;height: 100%;flex-direction: column;justify-content: start; align-items: center">
                    <el-row style="width: 100%; height: 10%; justify-content: end;padding: 10px 10px 0 0">
                        <el-button type="primary" ><el-icon><Refresh /></el-icon>刷新</el-button>
                    </el-row>
                    <el-row style="width: 100%; height: 90%">

                    </el-row>
                </el-row>
            </el-row>
            <el-row style="width: 100%; height: 70%;  background: #6e6775; border-radius: 10px;" class="card-eff">
                <el-row style="width: 100%;height: 100%;flex-direction: column;justify-content: start; align-items: center">
                    <el-row style="width: 100%; height: 10%; justify-content: end;padding: 10px 10px 0 0">
                        <el-button type="primary" ><el-icon><Refresh /></el-icon>刷新</el-button>
                    </el-row>
                    <el-row style="width: 100%; height: 90%">

                    </el-row>
                </el-row>
            </el-row>
        </el-row>
    </el-row>
</template>

<script setup lang="ts">

import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { FuzzStatType, ProjectType } from '@/types'
import { getProjectDetail } from '@/api/project'
import { DArrowRight, Refresh, Setting, VideoPause, VideoPlay } from '@element-plus/icons-vue'

const router = useRouter();
const route  = useRoute();
const projectId = route.query.projectId as string
const project_info = ref<ProjectType>();
const fuzz_stat = ref<FuzzStatType>({
    run_time: "0 days, 9 hrs, 47 min, 43 sec",
    last_new_path: "0 days, 0 hrs, 47 min, 31 sec",
    last_uniq_crash: "0 days, 3 hrs, 39 min, 58 sec",
    last_uniq_hang: "none seen yet",
    cycles_done: "97",
    total_path: "101",
    uniq_crashes: "8",
    uniq_hangs: "0",
    now_processing: "71* (70.30%)",
    paths_timed_out: "0 (0.00%)",
    map_density: "0.29% / 0.36%",
    count_coverage: "3.65 bits/tuple",
    now_trying: "splice 1",
    stage_execs: "66/240 (27.50%)",
    total_execs: "5.79M",
    exec_speed: "115.3/sec",
    favored_paths: "10 (9.90%)",
    new_edges_on: "16 (15.84%)",
    total_crashes: "4567 (8 unique)",
    total_tmouts: "3177 (15 unique)",
    bit_flips: "n/a, n/a, n/a",
    byte_flips: "n/a, n/a, n/a",
    arithmetics: "n/a, n/a, n/a",
    known_inis: "n/a, n/a, n/a",
    dictionary: "n/a, n/a, n/a",
    havoc: "55/2.08M, 53/3.68M",
    trim: "28.22%/41.9k, n/a",
    levels: "24",
    pending: "0",
    pend_fav: "0",
    own_finds: "100",
    imported: "n/a",
    stability: "100.00%",
    cpu: "cpu: 20%"
});
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