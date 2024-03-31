<template>
  <el-row style="flex-direction: column; justify-content: start; align-items: center;width: 100%; height: 100%; margin-top: 140px;">
    <el-row style="flex-direction: column; justify-content: center; align-items: center;width: 90%; height: fit-content; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19); border-radius: 10px; padding: 0 20px 50px 20px ">
      <el-avatar @click="onClickAvatar" :size="120" style="margin-top: -60px; box-shadow: 0 0px 5px 2px rgba(0, 0, 0, 0.19); margin-bottom: 30px; border-radius: 50%;" :src="bigAvatarSrc[0]"/>
      <el-row justify="center" align="middle">
        <span style="font-size: 35px; color: #313131; margin-bottom: 14px">{{UserInfo.userName}}</span>
<!--        <el-button size="small" round @click="" style="padding: 0 5px 0 5px"><el-icon><Edit /></el-icon></el-button>-->
      </el-row>
      <el-row justify="center" align="middle">
        <span style="font-size: 18px; color: #868686">{{UserInfo.signature}}</span>
<!--        <el-button size="small" round @click="" style="padding: 0 5px 0 5px"><el-icon><Edit /></el-icon></el-button>-->
      </el-row>

      <el-row style="width: 100%; height: fit-content; margin: 40px 0 0 0 ">
        <el-descriptions
          title="个人信息"
          border
          style="width: 100%"
          :column="2"
        >
          <template #extra>
            <el-button v-if="!isUpdatingProfile" size="small" @click="onClickEditProfileBtn">修改信息</el-button>
            <el-row v-else>
              <el-button size="small" type="success" @click="onClickCommitChangeProfileBtn">确认</el-button>
              <el-button size="small" type="danger" @click="onClickCancelChangeProfileBtn">取消</el-button>
            </el-row>
          </template>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165463_qr_code_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">用户ID</span>
                </el-row>
              </el-row>
            </template>
            <el-text>{{UserInfo.userId}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" :src="UserInfo.sex == 'male' ? '/icons/9165726_user_male_avatar_icon.png' : '/icons/9165712_user_female_avatar_icon.png'"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">用户名</span>
                </el-row>
              </el-row>
            </template>
            <el-input v-if="isUpdatingProfile" v-model="form.userName" placeholder="请输入用户名"/>
            <el-text v-else>{{UserInfo.userName}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" :src="UserInfo.sex == 'male' ? '/icons/9165411_male_gender_icon.png' : '/icons/9165554_femaile_gender_icon.png' "/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">性别</span>
                </el-row>
              </el-row>
            </template>
            <el-switch
                v-if="isUpdatingProfile"
              v-model="form.sex"
              inline-prompt
              style="--el-switch-on-color: #1a90e5; --el-switch-off-color: #d27373"
              active-text="男"
              inactive-text="女"
            />
            <el-text v-else>{{UserInfo.sex == 'male' ? '男' : '女'}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165561_mail_email_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">邮箱</span>
                </el-row>
              </el-row>
            </template>
            {{UserInfo.email}}
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165720_bell_alarm_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">手机</span>
                </el-row>
              </el-row>
            </template>
            <el-input v-if="isUpdatingProfile" v-model="form.phone" placeholder="请输入手机号码"/>
            <el-text v-else>{{UserInfo.phone}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165610_right_align_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">个性签名</span>
                </el-row>
              </el-row>
            </template>
            <el-input type="textarea" v-model="form.signature" v-if="isUpdatingProfile" placeholder="请输入个性签名"/>
            <el-text v-else>{{UserInfo.signature}}</el-text>
          </el-descriptions-item>
        </el-descriptions>
      </el-row>

      <el-row style="width: 100%; height: fit-content; margin: 40px 0 0 0 ">
        <el-descriptions
            title="预约平台信息"
            border
            style="width: 100%"
            :column="3"
        >
          <template #extra>
            <el-button size="small" @click="onClickUpdateUserInfoBtn">更新信息</el-button>

          </template>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165463_qr_code_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">学号</span>
                </el-row>
              </el-row>
            </template>
            <el-text>{{UserInfo.userInfo.username}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" :src="UserInfo.sex == 'male' ? '/icons/9165726_user_male_avatar_icon.png' : '/icons/9165712_user_female_avatar_icon.png'"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">姓名</span>
                </el-row>
              </el-row>
            </template>
            <el-text>{{UserInfo.userInfo.fullName}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item>
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165463_qr_code_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">学院</span>
                </el-row>
              </el-row>
            </template>
            <el-text>{{UserInfo.userInfo.department}}</el-text>
          </el-descriptions-item>

          <el-descriptions-item >
            <template #label>
              <el-row justify="start" align="middle">
                <el-image class="descriptions_icon" src="/icons/9165463_qr_code_icon.png"/>
                <el-row justify="center" align="middle" style="width: calc(100% - 26px)">
                  <span class="descriptions_label">Authorization</span>
                </el-row>
              </el-row>
            </template>
            <el-text>{{UserInfo.authorization.substring(0,50)+'......'}}</el-text>
          </el-descriptions-item>
        </el-descriptions>
      </el-row>

    </el-row>
  </el-row>

  <el-dialog
    v-model="updateAvatarDialogShow"
    width="90%"
    style="max-width: 800px;"
  >
    <template #header="{close, titleId, titleClass}">
      <el-row justify="center" align="middle" style="width: 100%">
        <span :id="titleId" :class="titleClass" style="font-size: 24px; color: #383838">修改头像</span>
      </el-row>
    </template>
    <el-row justify="center" align="middle" style="height: 100%; width: 100%">

      <el-tabs v-model="tabActivateName" style="width: 100%">
        <el-tab-pane label="插图" name="first">
          <el-divider content-position="left">用户上传</el-divider>

          <template v-for="(avatar, index) in avatarList.userHistoryFileList">
            <el-image style="width: 100px; height:100px" @click="onClickAvatarUpdate(avatar)" :src="userHistoryAvatarImgSrc[index]" />
          </template>


          <el-divider content-position="left">系统预设</el-divider>

          <template v-for="(avatar, index)  in avatarList.systemAvatarList">
            <el-image style="width: 100px; height:100px" @click="onClickAvatarUpdate(avatar)" :src="systemAvatarImgSrc[index]" />
          </template>

        </el-tab-pane>
        <el-tab-pane label="上传" name="second">
          <el-row style="justify-content: center; align-items: center; width: 100%; flex-direction: column">
            <el-upload
                class="avatar-uploader"
                :auto-upload="false"
                :on-change="handleUploadChanged"
                ref="uploadFile"
                :show-file-list="false"
            >
              <img v-if="uploadAvatarImageUrl" :src="uploadAvatarImageUrl" class="avatar" style="max-width: 300px; max-height: 300px; min-width: 178px; min-height: 178px;"/>
              <el-icon v-else style="width: 178px; height: 178px; border: 1px solid; border-style: dashed; border-radius: 5px;margin-bottom: 10px" class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <el-row>
              <el-button type="success" @click="onClickSubmitAvatarToServerBtn">确认</el-button>
            </el-row>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-row>
  </el-dialog>


  <el-dialog
      v-model="showGetCaptchaDialog"
      width="400"
      style="height: fit-content"
  >
    <p class="title">欢迎登陆<span class="s-desc">预约平台</span></p>
    <p>请在下方输入您ruc预约平台账号密码(账号密码不会被存储，请放心输入)</p>
    <el-form
        label-position='top'
        :model='captchaForm'
        :rules='loginCaptchaRules'
    >
      <el-form-item prop='username' >
        <el-input
            v-model='captchaForm.username'
            placeholder='用户名'
            class='login-input'
            size='large'

        />
      </el-form-item>
      <el-form-item prop='password'>
        <el-input
            v-model='captchaForm.password'
            type='password'
            show-password
            placeholder='密码'
            class='login-input'
            size='large'
        />
      </el-form-item>
      <el-form-item prop='password'>
       <el-row style="flex-wrap: nowrap; justify-content: space-between; align-items: center">
         <el-input
             v-model='captchaForm.captcha'
             type='password'
             show-password
             placeholder='验证码'
             class='login-input'
             size='large'
         />
         <el-image style="width: fit-content; height: fit-content" :src="'data:image/png;base64,'+captchaInfo.captchaText" />
       </el-row>
      </el-form-item>
      <el-row style='margin-top: 30px'>
        <el-button type='primary' @click="onClickPlatformLoginBtn" class="login-button">确认</el-button>
      </el-row>
    </el-form>
  </el-dialog>
</template>

<script setup lang="ts">
import {getUserInfo, setUserInfo} from "@/utils/auth.js";
import {onMounted, ref} from "vue";
import { changeUserProfile, userProfile, getAvatarListAPI, updateAvatarListAPI, getCaptchaInfo, updateUserAuthorization} from '@/api/user.js'
import {ElMessage, genFileId, UploadFile, UploadInstance, UploadProps, UploadRawFile} from "element-plus";
import {getFileObjByFileId, uploadFileAPI} from '@/api/file.js'
import {getImgSrcByFileObj, getImages, getImageBase64WithCache} from '@/utils/images'
import {Plus} from "@element-plus/icons-vue";
import {Base64} from "js-base64";

const tabActivateName = ref("first")
const updateAvatarDialogShow = ref(false)
const UserInfo = ref(getUserInfo())
const form = ref({
  userName: '',
  signature: '',
  sex: true,
  phone: ''
})

const showGetCaptchaDialog = ref(false)
const imgSrc = ref('')

const isUpdatingProfile = ref(false)


const uploadAvatarImageUrl = ref()
const uploadFile = ref()

const onClickEditUserNameBtn = () => {

}

const onClickEditSignatureBtn = () => {

}

const captchaForm = ref({
  username: '',
  password: '',
  captchaId: '',
  captcha: ''
})


const handleExceed: UploadProps['onExceed'] = (files) =>{
  uploadFile.value!.clearFiles()
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadFile.value!.handleStart(file);
}

const CurrentUploadAvatarFile = ref<UploadFile>()

const handleUploadChanged = (currentUploadFile: UploadFile, currentUploadFiles: UploadFiles) => {
  console.log("当前file")
  console.log(currentUploadFile)
  CurrentUploadAvatarFile.value = currentUploadFile;
  //检查是不是excel文件
  let fileName = currentUploadFile.name;
  let fileType = fileName.slice(fileName.lastIndexOf(".")+1);
  console.log("fileType = "+fileType)
  if(fileType !== "png" && fileType !== "jpg" && fileType !== "jpeg" && fileType !== "webp" && fileType !== "gif"){
    uploadFile.value!.clearFiles()
    ElMessage({
      message:"文件格式错误，请上传图片",
      type:"error"
    })
  }
  uploadAvatarImageUrl.value = URL.createObjectURL(currentUploadFile.raw)
}

const onClickSubmitAvatarToServerBtn = () => {
    let reader = new FileReader();
    reader.readAsDataURL(CurrentUploadAvatarFile.value.raw);
    let fileName = CurrentUploadAvatarFile.value.name;
    let isPrivate = false;
    reader.onload = (e) => {
      let result = e.target.result as string;
      let fileContent = result.slice(result.indexOf(','))
      // let fileContent = Base64.encode(result);
      uploadFileAPI(fileName, fileContent, 'avatar',false)
          .then((res) => {
            ElMessage({
              type:"success",
              message:res.msg
            })
            getAvatarList().then(() => {
              tabActivateName.value = 'first'
            })
          })
    }
}

const beforeAvatarUpload = (rawFile) => {
  return true;
}

const resetForm = () => {
  form.value.userName = UserInfo.value.userName
  form.value.signature = UserInfo.value.signature
  form.value.sex = UserInfo.value.sex == 'male' ? true : false
  form.value.phone = UserInfo.value.phone

  captchaForm.value.captchaId = ''
  captchaForm.value.captcha = ''
  captchaForm.value.username = ''
  captchaForm.value.password = ''
}

const onClickEditProfileBtn = () => {
  resetForm()
  isUpdatingProfile.value = true
}

const onClickCancelChangeProfileBtn = () => {
  resetForm()
  isUpdatingProfile.value = false
}

const onClickCommitChangeProfileBtn = () => {
  changeUserProfile(form.value)
      .then((res) => {
        getNewUserProfile().then(() => {
          UserInfo.value = getUserInfo()
          resetForm()
          ElMessage({
            type: 'success',
            message: "修改成功！"
          })
          isUpdatingProfile.value = false
        })
      })
}

const getNewUserProfile = () => {
  return userProfile().then((res) => {
    let userInfo = res.data.userInfo;
    setUserInfo(userInfo);
  })
}

const onClickAvatar = () => {
  getAvatarList().then(() => {
    updateAvatarDialogShow.value = true
  })

}

const avatarList = ref([])
const userHistoryAvatarImgSrc = ref(Array(100))
const systemAvatarImgSrc = ref(Array(100))
const getAvatarList = () => {
  return getAvatarListAPI()
      .then((res) => {
        avatarList.value = res.data
        let tmp1 = []
        let tmp2 = []

        for(let i = 0;i < avatarList.value.userHistoryFileList.length; ++i){
          getImageBase64WithCache(userHistoryAvatarImgSrc, i, avatarList.value.userHistoryFileList[i])
        }

        for(let i = 0;i < avatarList.value.systemAvatarList.length; ++i){
          getImageBase64WithCache(systemAvatarImgSrc, i, avatarList.value.systemAvatarList[i])
        }

      })
}


const onClickAvatarUpdate = (fileId) => {
  updateAvatarListAPI(fileId).then((res) => {
    ElMessage({
      type: "success",
      message: res.msg
    })
  }).then(()=>{
    updateAvatarDialogShow.value = false;
    getNewUserProfile().then(() => {
      location.reload();
    })
  })
}

const bigAvatarSrc = ref(Array(5))

const init_avatar = () => {
  getImageBase64WithCache(bigAvatarSrc, 0, UserInfo.value.avatar);
}

const onClickUpdateUserInfoBtn = () => {
  getCaptchaInfo().then(res => {
    captchaForm.value.captchaId =  res.data.captchaId
    captchaInfo.value.captchaId = res.data.captchaId
    captchaInfo.value.captchaText = res.data.captchaText
    showGetCaptchaDialog.value = true;
  })
}

const loginCaptchaRules = ref({
  username:[
    { required: true, message: "用户名不能为空", trigger: 'blur' },
  ],
  password:[
    { required: true, message: "密码不能为空", trigger: 'blur' },
  ],
  captcha:[
    { required: true, message: "验证码不能为空", trigger: 'blur' },
  ]
})

const captchaInfo = ref({})

const onClickPlatformLoginBtn  = () => {
  updateUserAuthorization(captchaForm.value).then(res => {
    getNewUserProfile().then(() => {
      UserInfo.value = getUserInfo()
      resetForm()
      ElMessage({
        type: 'success',
        message: "修改成功！"
      })
      showGetCaptchaDialog.value = false
    })
  })
}

onMounted(init_avatar)
</script>

<style scoped>
.descriptions_label{
  font-weight: bold;
  margin: 0 0 0 8px;
}

.descriptions_icon{
  width: 18px;
  height: 18px;
}

.title {
  font-size: 20px;
  color: #333;
  padding-bottom: 40px;
}
.s-desc {
  font-size: 14px;
  color: #999;
  padding-left: 5px;
}
/* 调整副标题文本颜色 */
.sutitle {
  font-size: 16px;
  color: #6e6775;
  padding-bottom: 10px;
}
.login-input {
  box-sizing: border-box;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
}
.login-input:focus {
  border-color: #007bff; /* 更改边框颜色 */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* 添加阴影效果 */
  outline: none; /* 去掉默认的外部轮廓线 */
}

.login-button {
  width: 100%;
  //background-color: #0056b3;
  //color: #fff;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
}

.bottom-click-text-btn:hover{
  color: #337ecc;
}

</style>
