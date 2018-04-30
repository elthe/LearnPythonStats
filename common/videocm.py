# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
Video common api
视频相关共通函数
"""

from moviepy.editor import *


def cut_save(src_path, start, end, target_path=None, fps=24):
    """
    截取视频指定片段并另存到指定文件。
    @param src_path: 视频源文件路径
    @param start: 开始坐标（第N秒）
    @param end: 结束坐标（第N秒）
    @param target_path: 视频目标文件路径，空则不另存
    @param fps: 输出文件每秒帧数
    @return: 截取后的视频片段
    """

    # 引入片头，可选
    src_clip = VideoFileClip(src_path)
    # 如果<0,则视为从末尾开始计算位置
    start = src_clip.duration + start if start < 0 else start
    end = src_clip.duration + end if end < 0 else end

    # 视频剪切
    target_clip = src_clip.subclip(start, end)

    # 生成目标视频文件
    if target_path is not None:
        target_clip.to_videofile(target_path, fps=fps, remove_temp=False)

    return target_clip


def concat_save(src_clips, target_path=None, fps=24):
    """
    合并视频片段并列表另存到指定文件。
    @param src_clips: 视频源文件路径
    @param target_path: 视频目标文件路径，空则不另存
    @param fps: 输出文件每秒帧数
    @return: 截取后的视频片段
    """

    # 拼接视频
    final_clip = concatenate_videoclips(src_clips)

    # 生成目标视频文件
    if target_path is not None:
        final_clip.to_videofile(target_path, fps=fps, remove_temp=False)

    return final_clip
