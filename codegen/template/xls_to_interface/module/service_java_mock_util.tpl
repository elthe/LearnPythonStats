package {{config.core_base_package}}.service.crm.util.{{config.package_sysname}}.{{module.moduleName}};

{% for c in module.services %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Req;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Resp;
{% endfor %}
import {{config.core_base_package}}.facade.code.RespCode;

/**
 * ClassName: {{module.moduleNameFcu}}MockUtil <br/>
 * Function: {{module.moduleDesc}}Mock数据共通工具类. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: {{module.codeCreateTime}} <br/>
 *
 * @author {{config.author}}
 * @version
 * @since JDK 1.7
 * {{config.copyrightEN}}
 * {{config.copyrightCN}}版权所有.
 */
public class {{module.moduleNameFcu}}MockUtil {

    {% for c in module.services %}
    /**
     * getMockDataOf{{c.className}}: {{c.name}}Mock数据生成. <br/>
     * 开始版本：{{c.startVersion}}.<br/>
     *
     * @author {{config.author}}
     * @param pReq
     * @return
     * @since JDK 1.7
     */
    public static {{c.className}}Resp getMockDataOf{{c.className}}({{c.className}}Req pReq) {
        {{c.className}}Resp lResp = new {{c.className}}Resp();
        lResp.setReqId(pReq.getReqId());
        lResp.setRespCode(RespCode.SUCCESS.getKey());
        lResp.setRespMessage(RespCode.SUCCESS.getValue());
        lResp.setSt(RespCode.STATUS_S.getKey());
        // TODO Mock数据组装
        {% for p in c.respProps %}
        /** {{p.name}} {{p.descFormat}} */
        // lResp.set{{p.idFcu}}("");
        {% endfor %}
        return lResp;
    }
    {% endfor %}

}