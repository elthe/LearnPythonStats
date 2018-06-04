package {{config.core_base_package}}.service.crm.impl.{{config.package_sysname}}.{{module.moduleName}};

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.github.miemiedev.mybatis.paginator.domain.PageList;
import {{config.com_package}}.common.cache.JedisCache;
import {{config.core_base_package}}.facade.abs.IRequest;
import {{config.core_base_package}}.facade.abs.IResponse;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{service.className}}Req;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{service.className}}Resp;
import {{config.core_base_package}}.facade.code.RespCode;
import {{config.core_base_package}}.facade.exception.BizException;
import {{config.core_base_package}}.facade.exception.ServiceException;
import {{config.core_base_package}}.service.rpc.AbstractRpcHandler;
import {{config.core_base_package}}.util.ConvertBeanUtil;
import {{config.core_base_package}}.util.log.LogPrinterTools;
import {{config.core_base_package}}.service.crm.util.{{config.package_sysname}}.{{module.moduleName}}.{{module.moduleNameFcu}}MockUtil;

/**
 * ClassName: LcsApp{{service.className}}Service <br/>
 * Function: {{service.desc}}. <br/>
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
public class {{config.core_base_service_prefix}}{{service.className}}Service extends AbstractRpcHandler<{{service.className}}Req> {
    private Logger mLogger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    protected JedisCache mJedisCache;

    @Override
    public Class<{{service.className}}Req> getObjectType() {
        return {{service.className}}Req.class;
    }

    @Override
    public void verifyParameter(IRequest pRequest) throws BizException {
        // {{service.className}}Req lReq = ({{service.className}}Req) pRequest;
        // String lReqId = lReq.getReqId();
    }

    @Override
    public IResponse handle(IRequest pRequest) throws ServiceException {
        {{service.className}}Req lReq = ({{service.className}}Req) pRequest;
        String lReqId = lReq.getReqId();
        {{service.className}}Resp lResp = new {{service.className}}Resp();
        try {
            // Mock数据处理
            lResp = {{module.moduleNameFcu}}MockUtil.getMockDataOf{{service.className}}(lReq);

        } catch (BizException e) {
            throw e;
        } catch (Exception e) {
            throw new ServiceException(RespCode.DB_EXCEPTION, e);
        }
        return lResp;
    }

    @Override
    public Object convertToDo(IRequest pRequest) {
        return null;
    }

    @Override
    public IResponse convertToDto(Object pValue) {
        return null;
    }

}