from aws_cdk import (
    core as cdk,
    aws_lambda,
    aws_route53,
    aws_apigateway
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
#from aws_cdk import core
#from aws_cdk.aws_apigatewayv2_integrations import LambdaProxyIntegration
#import aws_cdk.aws_apigatewayv2 as apigwv2
import aws_cdk.aws_certificatemanager as acm
from aws_cdk.aws_elasticloadbalancingv2 import TargetGroupBase
import aws_cdk.aws_route53_targets


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
        lambda_function_dev = aws_lambda.Function(
            self,
            id="lambda_function_dev",
            code=aws_lambda.Code.from_asset("./deploy_function_dev"),
            handler="lambda_function.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
        )
        
        cert_arn = "arn:aws:acm:us-east-1:209544401946:certificate/720b4dcc-e5d8-400b-9bbf-76e0fac4cbaa"
        domain_name = "indefensible.pub"
        certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn)

        lambda_integration = aws_apigateway.LambdaIntegration(lambda_function)
        lambda_integration_dev = aws_apigateway.LambdaIntegration(lambda_function_dev)

        api = aws_apigateway.RestApi(self,'redirect_api',
            default_integration=lambda_integration,
            domain_name=aws_apigateway.DomainNameOptions(
                domain_name=domain_name,
                certificate=certificate
            )
        )
        api_redirect_object = api.root.add_resource('redirect')
        api_redirect_object.add_method('GET')
        api_campaign_object = api_redirect_object.add_resource('{campaign}')
        api_campaign_object.add_method('GET')
        api_platform_object = api_campaign_object.add_resource('{platform}')
        api_platform_object.add_method('GET')

        api_dev_redirect_object = api.root.add_resource('redirect_dev')
        api_dev_redirect_object.add_method('GET',lambda_integration_dev)
        api_campaign_dev_object = api_dev_redirect_object.add_resource('{campaign}')
        api_campaign_dev_object.add_method('GET')
        api_platform_dev_object = api_campaign_dev_object.add_resource('{platform}')
        api_platform_dev_object.add_method('GET')

        aws_route53.ARecord(self, 'redirect_record',
            zone=aws_route53.HostedZone.from_hosted_zone_attributes(self, "HostedZone", 
                hosted_zone_id='Z0003169E7U99ETG4Y92',
                zone_name='indefensible.pub'
            ),
            target=aws_route53.RecordTarget.from_alias(aws_cdk.aws_route53_targets.ApiGateway(api))
        )








        #dn = apigwv2.DomainName(
        #    self,
        #    "DN",
        #    domain_name=domain_name,
        #    certificate=acm.Certificate.from_certificate_arn(self, "cert", cert_arn),
        #)
#
        #http_api = apigwv2.HttpApi(self, "indefensible_redirect", 
        #default_domain_mapping=apigwv2.DomainMappingOptions(
        #        domain_name=dn
        #    ))
#
        #http_api.add_routes(
        #    path="/redirect",
        #    methods=[apigwv2.HttpMethod.GET],
        #    integration=lambda_function_integration,
        #)
        #record = aws_route53.ARecord(self, 'IndefensibleARecord',
        #    zone=aws_route53.HostedZone.from_hosted_zone_attributes(self, "HostedZone", 
        #        hosted_zone_id='Z0003169E7U99ETG4Y92',
        #        zone_name='indefensible.pub'
        #    ),
        #    record_name='api',
        #    target=aws_route53.RecordTarget.from_alias(aws_cdk.aws_route53_targets.ApiGatewayv2DomainProperties(str(http_api.api_id)+'.execute-api.us-east-1.amazonaws.com', dn.regional_hosted_zone_id))
        #)
#