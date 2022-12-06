@REM Train models
@REM 
@REM 

@REM Train data owner A's model, test basic functionality
python ./core/ai/train.py --id A --modules "LazyBatchNorm1d() | LazyLinear(128) | GELU()"

@REM Train data owner B's model, test less number of epochs and training with cpu
python ./core/ai/train.py --id B --modules "LazyBatchNorm1d() | LazyLinear(128) | GELU()" --epochs 3 --cpu

@REM Train data owner C's model, test larger model
python ./core/ai/train.py --id C --modules "LazyBatchNorm1d() | LazyLinear(256) | GELU()"

@REM Train data owner D's model, test a different learning rate
python ./core/ai/train.py --id D --modules "LazyBatchNorm1d() | LazyLinear(128) | GELU()" --lr 0.005

@REM Train data owner E's model, test a model with extra layers
python ./core/ai/train.py --id E --modules "LazyBatchNorm1d() | LazyLinear(128) | GELU() | LazyLinear(64) | GELU()"

@REM Train data owner F's model, test a model without normalization
python ./core/ai/train.py --id F --modules "LazyLinear(128) | GELU()"

@REM Train data owner G's model, test the largest model
python ./core/ai/train.py --id G --modules "LazyBatchNorm1d() | LazyLinear(256) | GELU() | LazyLinear(64) | GELU()" --epochs 15

@REM Train data owner T1's model, 
python ./core/ai/train.py --id T1 --modules "LazyBatchNorm1d() | LazyLinear(32) | GELU()" --epochs 3

@REM Train data owner T2's model, 
python ./core/ai/train.py --id T2 --modules "LazyBatchNorm1d() | LazyLinear(64) | GELU()"

@REM Train data owner T3's model, 
python ./core/ai/train.py --id T3 --modules "LazyBatchNorm1d() | LazyLinear(32) | GELU()" --epochs 3

