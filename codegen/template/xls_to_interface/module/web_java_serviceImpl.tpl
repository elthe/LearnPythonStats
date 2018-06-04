package {{config.base_package}}.service.{{module.moduleName}}.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import {{config.com_package}}.common.cache.JedisCache;
import {{config.core_base_package}}.facade.abs.AbstractDubboResponse;
{% for c in module.services %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Req;
{% endfor %}
import {{config.base_package}}.service.{{module.moduleName}}.I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service;
import {{config.base_package}}.util.log.LogInfoConstant;
import {{config.base_package}}.util.log.LogPrinterTools;
import {{config.base_package}}.web.result.LcsAppResultVo;
import {{config.com_package}}.exception.ServiceException;
import {{config.com_package}}.integration.dobbo.o2o.crm.ILcsAppServiceFacadeClient;

/**
* ClassName: {{config.base_service_prefix}}{{module.moduleNameFcu}}ServiceImpl <br/>
* Function: {{module.moduleDesc}}接口实现类. <br/>
* Reason: TODO ADD REASON. <br/>
* Date: {{module.codeCreateTime}} <br/>
*
* @author {{config.author}}
* @version
* @since JDK 1.7
* {{config.copyrightEN}}
* {{config.copyrightCN}}版权所有.
*/
@Service
public class {{config.base_service_prefix}}{{module.moduleNameFcu}}ServiceImpl implements I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service {
    private final Logger mLogger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private ILcsAppServiceFacadeClient mLcsAppFacadeClient;

    @Autowired
    protected JedisCache mJedisCache;

    {% for c in module.services %}
    @Override
    public LcsAppResultVo {{c.methodName}}({{c.className}}Req pReq) {

        String lReqId = pReq.getReqId();
        AbstractDubboResponse lResp = null;
        try {
            // 调用CRM核心
            lResp = mLcsAppFacadeClient.execution(pReq);

            return LcsAppResultVo.createSuccessResultVo(lResp);

        } catch (ServiceException e) {
            // 监控日志
            String lErrorCode = LogInfoConstant.errorCode_S01;
            String lErrorMessage = e.getMessage();
            LogPrinterTools.printMonitorServiceError(mLogger, lReqId, lErrorCode, lErrorMessage, e,
            LogInfoConstant.monitorCodeError_001);

            return LcsAppResultVo.createSystemErrorResultVo(lErrorMessage);
        }
    }

    {% endfor %}
}