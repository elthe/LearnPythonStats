package {{config.base_package}}.controller.{{module.moduleName}};

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;

import com.google.gson.Gson;
{% for c in module.services %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.methodName|capitalize}}Req;
{% endfor %}
import {{config.base_package}}.controller.LcsAppBaseController;
import {{config.base_package}}.service.{{module.moduleName}}.I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service;
import {{config.base_package}}.util.log.LogPrinterTools;
import {{config.base_package}}.web.result.LcsAppResultVo;

/**
 * ClassName: {{config.base_controller_prefix}}{{module.moduleNameFcu}}Controller <br/>
 * Function: {{module.moduleDesc}}控制器. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: {{module.codeCreateTime}} <br/>
 *
 * @author {{config.author}}
 * @version
 * @since JDK 1.7
 * {{config.copyrightEN}}
 * {{config.copyrightCN}}版权所有.
 */
@Controller
@RequestMapping("/{{config.controller_path}}")
public class {{config.base_controller_prefix}}{{module.moduleNameFcu}}Controller extends LcsAppBaseController {
    
    private Logger mLogger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service m{{module.moduleNameFcu}}Service;

    {% for c in module.services %}
    /**
    * {{c.methodName}}: {{c.name}}. <br/>
    * 说明： {{c.desc}}.<br/>
    * 开始版本：{{c.startVersion}}.<br/>
    *
    * @author {{config.author}}
    * @param pRequest
    * @param pResponse
    * @param pModel
    * @return
    * @since JDK 1.7
    */
    @RequestMapping("/{{c.interfaceName}}")
    public String {{c.methodName}}(HttpServletRequest pRequest, HttpServletResponse pResponse, ModelMap pModel) {
    long lStartTime = System.currentTimeMillis();
    String lReqId = getReqId();
    {% if c.hasReqData %}
    // 取得加密参数
    {{c.methodNameFcu}}Req lReq = new Gson().fromJson((String) pRequest.getAttribute("data"), {{c.methodNameFcu}}Req.class);
    {% elif not c.hasReqData %}
    // 没有加密参数
    {{c.methodNameFcu}}Req lReq = new {{c.methodNameFcu}}Req();
    {% endif %}
    lReq.setReqId(lReqId);

    // 设置共通请求参数
    setLcsAppCommonReq(pRequest, lReq);
    LogPrinterTools.printReqStart(mLogger, lReqId, lReq);

    // {{c.name}}
    LcsAppResultVo lResultVo = m{{module.moduleNameFcu}}Service.{{c.methodName}}(lReq);

    LogPrinterTools.printObject(mLogger, lReqId, "lResultVo", lResultVo);
    String lResponseStr = render(lResultVo);
    pModel.put("json", lResponseStr);
    long lCostTime = (System.currentTimeMillis() - lStartTime);
    LogPrinterTools.printReqEnd(mLogger, lReqId, lResultVo, lCostTime);
    return "json";
    }
    {% endfor %}
}