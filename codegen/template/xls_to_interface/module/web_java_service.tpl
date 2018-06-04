package {{config.base_package}}.service.{{module.moduleName}};

{% for c in module.services %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Req;
{% endfor %}
import {{config.base_package}}.web.result.LcsAppResultVo;

/**
* ClassName: I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service <br/>
* Function: {{module.moduleDesc}}接口定义类. <br/>
* Reason: TODO ADD REASON. <br/>
* Date: {{module.codeCreateTime}} <br/>
*
* @author {{config.author}}
* @version
* @since JDK 1.7
* {{config.copyrightEN}}
* {{config.copyrightCN}}版权所有.
*/
public interface I{{config.base_service_prefix}}{{module.moduleNameFcu}}Service {

    {% for c in module.services %}
    /**
     * {{c.methodName}}: {{c.desc}}.
     *
     * @author {{config.author}}
     * @param pReq
     * @return
     * @since JDK 1.7
     */
    LcsAppResultVo {{c.methodName}}({{c.className}}Req pReq);

    {% endfor %}
}