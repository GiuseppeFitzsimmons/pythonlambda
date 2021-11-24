from aws_cdk import (
    core as cdk,
    aws_lambda,
    aws_route53
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk.aws_apigatewayv2_integrations import LambdaProxyIntegration
import aws_cdk.aws_apigatewayv2 as apigwv2
import aws_cdk.aws_certificatemanager as acm


class CdkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = aws_lambda.Function(
            self,
            id="lambda_function",
            code=aws_lambda.Code.from_asset("./deploy_function"),
            handler="lambda_function.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )

        lambda_function_integration = LambdaProxyIntegration(handler=lambda_function)
        
        cert_arn = "arn:aws:acm:us-east-1:209544401946:certificate/720b4dcc-e5d8-400b-9bbf-76e0fac4cbaa"
        domain_name = "indefensible.pub"

        dn = apigwv2.DomainName(
            self,
            "DN",
            domain_name=domain_name,
            certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn),
        )

        http_api = apigwv2.HttpApi(self, "indefensible_redirect", 
        default_domain_mapping=apigwv2.DomainMappingOptions(
                domain_name=dn, 
                #mapping_key="foo"
            ))

        http_api.add_routes(
            path="/redirect",
            methods=[apigwv2.HttpMethod.GET],
            integration=lambda_function_integration,
        )

        record = aws_route53.ARecord(self, 
            zone='us-east-1',
            record_name='www',
            target=aws_route53.RecordTarget.from_alias(apigwv2.DomainNameAttributes(dn.regional_domain_name, dn.regional_hosted_zone_id))
        )


        #api = apigwv2.HttpApi(
        #    self,
        #    "HttpProxyProdApi",
        #    default_integration=LambdaProxyIntegration(handler=lambda_function),
        #    # https://${dn.domainName}/foo goes to prodApi $default stage
        #    default_domain_mapping=apigwv2.DomainMappingOptions(
        #        domain_name=dn, mapping_key="foo"
        #    ),
        #)
