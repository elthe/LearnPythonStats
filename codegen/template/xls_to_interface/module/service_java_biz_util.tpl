package {{config.core_base_package}}.service.crm.util.{{config.package_sysname}}.{{module.moduleName}};

{% for c in module.services %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Req;
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}}Resp;
{% endfor %}
import {{config.core_base_package}}.facade.code.RespCode;

/**
 * ClassName: {{module.moduleNameFcu}}BizUtil <br/>
 * Function: {{module.moduleDesc}}业务数据共通工具类. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: {{module.codeCreateTime}} <br/>
 *
 * @author {{config.author}}
 * @version
 * @since JDK 1.7
 * {{config.copyrightEN}}
 * {{config.copyrightCN}}版权所有.
 */
public class {{module.moduleNameFcu}}BizUtil {



}