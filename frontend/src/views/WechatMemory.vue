<template>
  <el-row style="height: 100%; width: 100%;flex-direction: row; justify-content: start ; overflow-y: auto">
    <el-row class="topImage">
      <el-image style="width: 100%; height: 400px;" src="/purpleImg_title.jpg" />
    </el-row>
    <el-divider content-position="center" style="font-weight: bold">Wechat Memory Analysis Result</el-divider>
    <el-row style="flex-direction: row; justify-content: space-between; width: 100%">
      <el-row style="flex-direction: column;">
        <el-row class="item">
          <el-text  class="item_title" >聊天词云图（我的）</el-text>
        </el-row>
        <el-divider border-style="dashed" />
        <el-row class="item">
          <el-text  class="item_title" >吵架时间分布图</el-text>
        </el-row>
        <el-divider border-style="dashed" />
        <el-row class="item">
          <el-text  class="item_title" >心情分布图</el-text>
        </el-row>
      </el-row>
      <el-row style="flex-direction: column; ">
        <el-row class="item">
          <el-text  class="item_title">聊天词云图（ta的）</el-text>
        </el-row>
        <el-divider border-style="dashed" />
        <el-row class="item">
          <el-text  class="item_title">频繁出现的emoji</el-text>
        </el-row>
        <el-divider border-style="dashed" />
        <el-row class="item">
          <el-text  class="item_title">爱用表情包</el-text>
        </el-row>
      </el-row>

    </el-row>
  </el-row>
</template>

<script setup>
</script>

<style scoped>
.topImage{
  align-items: center;
  width: 100%;
  height: 400px;
}
.item_title{
  font-size: 30px;
  font-family: "LXGW WenKai Mono Bold";
  font-weight: 8;
  color: rgba(23, 23, 24, 0.85);
  margin-top: 5px;
}
.item{
  width: 615px;
  height: fit-content;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content: start;
  margin: 5px;
  border-radius: 5px;
  //border-top: 2px solid rgba(23, 23, 24, 0.75);
  //border-bottom: 2px solid rgba(23, 23, 24, 0.75);
  //border-left: 1px solid rgba(23, 23, 24, 0.75);
  //border-right: 1px solid rgba(23, 23, 24, 0.75);
}
</style>