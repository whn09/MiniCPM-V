// 定时发送消息
// export const sendMessage = data => {
//     return useHttp.post('/api/v1/stream', data);
// };
export const sendMessage = async data => {
    const start = Date.now();
    try {
        const result = await useHttp.post('/api/v1/stream', data);
        const timeSpent = Date.now() - start;
        console.log(`sendMessage took ${timeSpent}ms`);
        return result;
    } catch (error) {
        const timeSpent = Date.now() - start;
        console.log(`sendMessage failed after ${timeSpent}ms`);
        throw error;
    }
};
// 跳过当前
export const stopMessage = () => {
    return useHttp.post('/api/v1/stop');
};
// 上传音色文件
export const uploadFile = data => {
    return useHttp.post('/api/v1/upload_audio', data);
};
// 反馈
export const feedback = data => {
    return useHttp.post('/api/v1/feedback', data);
};
// 上传配置
export const uploadConfig = data => {
    return useHttp.post('/api/v1/init_options', data);
    // return useHttp.post('/api/v1/upload_audio', data);
};
