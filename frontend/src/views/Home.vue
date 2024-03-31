
<template>

  <el-row style="width: 100%; height: 100%; justify-content: center; align-items: start">
    <el-row style="width: 80%; height: 100%; margin: 30px 10px 30px 10px; flex-direction: column; justify-content: start; align-items: center; flex-wrap: nowrap">

      <el-row style="width: 100%; height: fit-content; padding: 20px 10px 20px 10px;  justify-content: end; align-items: center">
        <el-button type="primary" plain style="float:right; margin-right: 5px;" @click="onClickAddTaskBtn">新建任务</el-button>
        <el-badge :value="multipleSelectedUser.length">
          <el-button type="danger" plain style="float:right; margin-left: 5px;" @click="onClickDeleteTaskBtn">删除选中任务</el-button>
        </el-badge>
      </el-row>

      <el-row  style="width: 100%; height: 100%; justify-content: center">
        <el-table
            :data="table_data"
            highlight-current-row
            stripe
            @selection-change="handleSelectionChange"
            :default-sort="{ prop: 'userId', order: 'descending'}"
            style="width: 100%"
        >
          <el-table-column type="selection"/>
          <el-table-column prop="task_id" label="ID"/>
          <el-table-column prop="time_start" label="最早开始时间"/>
          <el-table-column prop="time_end" label="最晚开始时间"/>
          <el-table-column prop="onDate" label="预约日期"/>
          <el-table-column prop="length" label="最短使用时长"/>
          <el-table-column prop="room_type" label="静音仓类型"/>
          <el-table-column prop="interval_ms" label="请求间隔"/>
          <el-table-column prop="favored_venue" label=""/>
        </el-table>
      </el-row>

      <el-row class="flex flex_direction_row_reverse ">
        <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 25, 50, 75, 100]"
            :background="true"
            layout="sizes, prev, pager, next"
            :total="total_table_data.length"
            @size-change="changeTableDataByPagePageSize"
            @current-change="changeTableDataByPagePageSize"
        />
      </el-row>
    </el-row>
  </el-row>


  <el-dialog
    v-model="showConfigTaskDialog"
    title="导入任务"
    style="width: fit-content"
  >
    <el-row>
      <el-form v-model="form" label-width="180px">
        <el-form-item label="预约日期">
          <el-date-picker
              v-model="form.onDate"
              style="width: fit-content"
              placeholder="预约日期"
            :disabled-date="checkDisabledDate"
          />
        </el-form-item>
        <el-form-item label="开始的时间范围">
          <el-row style="justify-content: start; align-items: center;flex-wrap: nowrap">
            <el-select
                v-model="form.time_start"
                placeholder="最早开始时间"
                style="width: 180px"
            >
              <el-option
                  v-for="item in availableTimeList"
                  :key="item"
                  :label="item"
                  :value="item"
              />
            </el-select>
            -
            <el-select
                v-model="form.time_end"
                placeholder="最晚开始时间"
                style="width: 180px"
            >
              <el-option
                  v-for="item in availableTimeList"
                  :key="item"
                  :label="item"
                  :value="item"
              />
            </el-select>
          </el-row>
        </el-form-item>

        <el-form-item label="希望使用的最短时长(min)">
          <el-row style="justify-content: start; align-items: center;flex-wrap: nowrap">
            <el-select
                v-model="form.length"
                placeholder="选择希望使用的最短时长(min)"
                style="width: 240px"
            >
              <el-option
                  v-for="item in [30, 60, 90, 120, 150, 180, 210, 240]"
                  :key="item"
                  :label="item"
                  :value="item"
              />
            </el-select>
          </el-row>
        </el-form-item>

        <el-form-item label="请求间隔(ms)">
          <el-row style="justify-content: start; align-items: center;flex-wrap: nowrap">
            <el-input type="number" placeholder="请求间隔(ms)" v-model="form.interval_ms" />
          </el-row>
        </el-form-item>

        <el-form-item label="静音仓类型">
          <el-row style="justify-content: start; align-items: center;flex-wrap: nowrap">
            <el-select
                v-model="form.room_type"
                placeholder="静音仓类型"
                style="width: 240px"
            >
              <el-option
                  v-for="item in availableRoomType"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-row>
        </el-form-item>

        <el-form-item label="教学楼">
          <el-row style="justify-content: start; align-items: center;flex-wrap: nowrap; align-items: start; flex-direction: column">
            <el-row v-for="(item, index) in form.favored_venue" style="justify-content: start; align-items: center; margin:  5px 0px 5px 0px">
              <el-select
                  v-model="form.favored_venue[index]"
                  placeholder="请选择一个教学楼"
                  style="width: 240px; margin-right: 5px"
              >
                <el-option
                    v-for="item in availableVenue"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                />
              </el-select>
              <el-button type="success" plain circle @click="onClickAddVenueBtn(index)" style="text-align: center; font-size: 20px">+</el-button>
              <el-button  v-if="form.favored_venue.length > 1" plain  style="text-align: center; font-size: 20px" type="danger" circle @click="onClickDelVenueBtn(index)">-</el-button>
            </el-row>
          </el-row>
        </el-form-item>
      </el-form>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="danger" plain @click="onClickCancelBtn">取消</el-button>
        <el-button type="success" plain @click="onClickCommitBtn">确认</el-button>
      </span>
    </template>
  </el-dialog>

</template>

<script setup lang="js">
import { reactive, ref } from 'vue'
import { onMounted } from 'vue'
import { listTask, delTask, updateTask, getRoomList, getRoomTypeList, getVenueList, addTask, getOpenDateList } from "@/api/task.js";
import {ElMessage, ElMessageBox} from "element-plus";

const multipleSelectedUser = ref([])
const table_data = ref([])
const total_table_data = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const showConfigTaskDialog = ref(false)
const isUpdateTask = ref(false)
const availableDays = ref([])
const availableRoomType = ref([])
const availableVenue = ref([])

const availableTimeList = ref([])

const form = ref([{
  time_start: "",
  time_end: "",
  onDate: "",
  length: 30,
  favored_venue: [""],
  room_type: "",
  interval_ms: 1000,
  task_id: ""
}])

const resetForm = () => {
  form.value.time_start = ""
  form.value.time_end = ""
  form.value.onDate = ""
  form.value.favored_venue = [""]
  form.value.length = 30
  form.value.room_type = ""
  form.value.interval_ms = 1000
  form.value.task_id = ""
}

const onClickAddTaskBtn = () => {
  resetForm();
  showConfigTaskDialog.value = true;
}

const onClickDeleteTaskBtn = () => {
  let confimMessage = "下列任务将被永久删除，你确定吗？\n";
  multipleSelectedUser.value.forEach(item => {
    confimMessage += item.userId + " "
  })
  ElMessageBox.confirm(
      confimMessage,
      'Warning',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
  ).then(() => {
    multipleSelectedUser.value.forEach(item => {
      deleteStudent(item);
    })
  }).catch(()=>{

  })
}
function handleSelectionChange(val){
  multipleSelectedUser.value = val;
}

function changeTableDataByPagePageSize(){
  let tarPage = currentPage.value;
  let tarPageSize = pageSize.value;
  table_data.value = total_table_data.value.slice((tarPage-1)*tarPageSize, tarPage*tarPageSize)
}

function loadinfo(){
  listTask().then((res) => {
    total_table_data.value = res.data;
    changeTableDataByPagePageSize();
  })
  getOpenDateList().then(res => {
    let tmp_list = res.data
    availableDays.value = []
    tmp_list.forEach(item => {
      availableDays.value.push(new Date(Date.parse(item)))
    })
  })
  getVenueList().then(res => {
    availableVenue.value = res.data
  })
  getRoomTypeList().then(res => {
    availableRoomType.value = res.data
  })
  availableTimeList.value = []
  for(let i = 8; i < 22;i++){
    availableTimeList.value.push(`${i.toFixed(0).padStart(2,'0')}:00`)
    availableTimeList.value.push(`${i.toFixed(0).padStart(2,'0')}:30`)
  }
}

const checkDisabledDate = (time) => {
  for(let i = 0; i < availableDays.value.length; i++){
    let item = availableDays.value[i];
    if(time.getFullYear() == item.getFullYear() && time.getMonth() == item.getMonth() && time.getDate() == item.getDate()){
      return false;
    }
  }
  return true;
}

const onClickAddVenueBtn = (index) => {
  form.value.favored_venue.splice(index+1,0,"")
}

const onClickDelVenueBtn = (index) => {
  form.value.favored_venue.splice(index, 1)
}

const onClickCommitBtn  = () => {
  if(isUpdateTask.value){
    updateTask(form.value).then(res => {
      ElMessage({
        type: "success",
        message: res.msg
      });
    })
  }else{
    addTask(form.value).then(res => {
      ElMessage({
        type: "success",
        message: res.msg
      });
    })
  }
}

const onClickCancelBtn = () => {
  resetForm();
  showConfigTaskDialog.value = false;
}


onMounted(loadinfo)
</script>


<style scoped>


</style>
